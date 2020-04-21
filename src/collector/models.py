from django.db import models
from utils.models import BaseTimeStampField
# Create your models here.
from django.utils.decorators import classonlymethod
import os
from django.utils.timezone import now
import uuid
from django.core.files.base import ContentFile
import json
from celery import chain
from django.conf import settings
from django.utils.functional import cached_property
from django.contrib.postgres.fields import HStoreField



class EmailBodyTypeChoice:
    HTML = 'h'
    TEXT = 'T'

    @classonlymethod
    def get_choices(cls):
        return (
            (cls.HTML, 'HTML'),
            (cls.TEXT, 'Text')
        )



EMAIL_BODY_TYPE_LIST = EmailBodyTypeChoice.get_choices()


class TemplateMatchStatusChoice:
    NEW = 'NEW'
    MULTIPLE_TEMPLATE_MATCH = 'MULTIPLE_MATCH'
    NO_TEMPLATE_MATCH = 'NOT_MATCH'
    TEMPLATE_MATCH_FOUND = 'MATCH_FOUND'

    @classonlymethod
    def get_choices(cls):
        return (
            (cls.NEW, 'New'),
            (cls.MULTIPLE_TEMPLATE_MATCH, 'Multiple template match found'),
            (cls.NO_TEMPLATE_MATCH, 'No template match found'),
            (cls.TEMPLATE_MATCH_FOUND, 'Template matched')
        )


TEMPLATE_MATCH_STATUS_CHOICE_LIST = TemplateMatchStatusChoice.get_choices()


class EmailCollection(BaseTimeStampField):

    def get_upload_location(instance, filename):
        d = now().strftime("%Y%m%d")
        return "emails/{}/{}/{}".format(d, instance.pk, filename)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.FileField(upload_to=get_upload_location, null=True, blank=True)
    email_from = models.EmailField()
    subject = models.CharField(max_length=256, blank=True)
    template_match_status = models.CharField(max_length=15,
                                             default=TemplateMatchStatusChoice.NEW,
                                             choices=TEMPLATE_MATCH_STATUS_CHOICE_LIST)
    template = models.ForeignKey('parsers.Template',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    meta = HStoreField(verbose_name="Extracted data", null=True)
    is_published = models.BooleanField(default=False, editable=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'email'
        verbose_name_plural = 'emails'

    def __str__(self):
        return str(self.email_from)

    def save(self,  *args,  **kwargs):
        created = self._state.adding
        super(EmailCollection, self).save(*args, **kwargs)
        if created:
            from .tasks import MatchTemplateTask, \
                ExecuteParserTask
                #, PublishToSBTask
            match_template = MatchTemplateTask()
            execute_parser_task = ExecuteParserTask()
            # publish_to_sb_task = PublishToSBTask()
            c = chain(match_template.s(), execute_parser_task.s())
            c.delay(self.pk)

    @cached_property
    def read_email_from_file(self):
        if self.location:
            with open(self.location.path) as f:
                f_con = json.load(f)
            return f_con

    @property
    def body(self):
        if self.read_email_from_file:
            return self.read_email_from_file.get('text')

    @property
    def email_to(self):
        if self.read_email_from_file:
            return self.read_email_from_file.get('to')

    @property
    def attachment_info(self):
        if self.read_email_from_file:
            attachments = self.read_email_from_file.get('attachment-info')
            return attachments

    @property
    def email_date(self):
        if self.read_email_from_file:
            headers = self.read_email_from_file.get('headers')
            email_date = headers[int(headers.find("Date:")):int(headers.find("Message-ID"))].split("Date:")[-1].split("\n")[
                0].lstrip()
            return email_date
        else:
            return ''

    @property
    def sender_ip(self):
        if self.read_email_from_file:
            return self.read_email_from_file.get('sender_ip')


    @property
    def html(self):
        if self.read_email_from_file:
            ### body should be in HTML
            return self.read_email_from_file.get('html')

    @property
    def headers(self):
        if self.read_email_from_file:
            return self.read_email_from_file.get('headers')

    @property
    def envelope(self):
        if self.read_email_from_file:
            return self.read_email_from_file.get('envelope')

    @property
    def dkim(self):
        if self.read_email_from_file:
            return self.read_email_from_file.get('dkim')

    @property
    def content_ids(self):
        if self.read_email_from_file:
            return self.read_email_from_file.get('content-ids')

    @property
    def charsets(self):
        if self.read_email_from_file:
            return self.read_email_from_file.get('charsets')

    @property
    def cc(self):
        if self.read_email_from_file:
            return self.read_email_from_file.get('cc')

    @property
    def attachments_count(self):
        if self.read_email_from_file:
            return self.read_email_from_file.get('attachments')

    @property
    def spf(self):
        if self.read_email_from_file:
            return self.read_email_from_file.get('SPF')

    @property
    def body_type(self):
        if self.read_email_from_file:
            body_type = None
            if self.read_email_from_file.get('text'):
                body_type = 'text'
            elif self.read_email_from_file.get('html'):
                body_type = 'html'
            return body_type

    def publish_order(self):
        try:
            self.template.desination.publish(self)
            self.is_published = True
            self.save()
        except Exception as e:
            print(e)
            self.is_published = False
            self.save()


class EmailAttachment(BaseTimeStampField):
    def get_upload_location(instance, filename):
        d = now().strftime("%Y%m%d")
        return "emails/{}/{}/{}/".format(d, instance.email.pk, filename)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.ForeignKey(EmailCollection, on_delete=models.CASCADE)
    location = models.FileField(upload_to=get_upload_location)

    def __str__(self):
        return str(self.email.email_from)
