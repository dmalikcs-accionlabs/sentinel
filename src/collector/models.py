from django.db import models
from utils.models import BaseTimeStampField
# Create your models here.
from django.utils.decorators import classonlymethod
import os
from django.utils.timezone import now
from azure.servicebus import QueueClient, Message, ServiceBusClient
import uuid
from django.core.files.base import ContentFile
import json
from celery import chain
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.utils.functional import cached_property

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


class EmailCollection(BaseTimeStampField):

    def get_upload_location(instance, filename):
        d = now().strftime("%Y%m%d")
        return "emails/{}/{}/{}".format(d, instance.pk, filename)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.FileField(upload_to=get_upload_location, null=True, blank=True)
    email_from = models.EmailField()
    subject = models.CharField(max_length=256, blank=True)
    template = models.ForeignKey('parsers.Template',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    parser = models.ForeignKey('parsers.ParsingTask',
                               on_delete=models.SET_NULL, null=True, blank=True)
    is_published = models.BooleanField(default=False, editable=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.email_from)

    def save(self,  *args,  **kwargs):
        created = self._state.adding
        super(EmailCollection, self).save(*args, **kwargs)
        if created:
            from .tasks import MatchTemplateTask, \
                ExecuteParserTask, PublishToSBTask
            match_template = MatchTemplateTask()
            execute_parser_task = ExecuteParserTask()
            publish_to_sb_task = PublishToSBTask()
            c = chain(match_template.s(), execute_parser_task.s(), publish_to_sb_task.s())
            c.delay(self.pk)

    @cached_property
    def read_email_from_file(self):
        with open(self.location.path) as f:
            f_con = json.load(f)
        return f_con

    @property
    def body(self):
        #  todo: update form json
        return self.read_email_from_file.get("text")

    @property
    def body(self):
        return self.read_email_from_file.get('text')

    @property
    def email_to(self):
        return self.read_email_from_file.get('to')

    @property
    def attachment_info(self):
        attachments = self.read_email_from_file.get('attachment-info')
        return attachments

    @property
    def email_date(self):
        headers = self.read_email_from_file.get('headers')
        email_date = headers[int(headers.find("Date:")):int(headers.find("Message-ID"))].split("Date:")[-1].split("\n")[
            0].lstrip()
        return email_date

    @property
    def sender_ip(self):
        return self.read_email_from_file.get('sender_ip')

    @property
    def subject(self):
        return self.read_email_from_file.get('subject')

    @property
    def html(self):
        return self.read_email_from_file.get('html')

    @property
    def headers(self):
        return self.read_email_from_file.get('headers')

    @property
    def envelope(self):
        return self.read_email_from_file.get('envelope')

    @property
    def dkim(self):
        return self.read_email_from_file.get('dkim')

    @property
    def content_ids(self):
        return self.read_email_from_file.get('content-ids')

    @property
    def charsets(self):
        return self.read_email_from_file.get('charsets')

    @property
    def cc(self):
        return self.read_email_from_file.get('cc')

    @property
    def attachments_count(self):
        return self.read_email_from_file.get('attachments')

    @property
    def spf(self):
        return self.read_email_from_file.get('SPF')

    def publish_order(self, order_id):
        if not (settings.AZURE_SB_CONN_STRING and settings.AZURE_SB_CANCEL_QUEUE):
            print("Azure service bus in not configured properly")
            return
        connection_str = settings.AZURE_SB_CONN_STRING
        sb_client = ServiceBusClient.from_connection_string(connection_str)
        queue_client = sb_client.get_queue(settings.AZURE_SB_CANCEL_QUEUE)
        queue_client.send(Message(json.dumps({
            "CreationDate": self.created_at,
            "MessageType": 0,
            "Content": {
                "SenderAddress": self.email_from,
                "EmailDate": self.email_date,
                "OrderNumber": order_id
            }
        }, cls=DjangoJSONEncoder), ))


class EmailAttachment(BaseTimeStampField):
    def get_upload_location(instance, filename):
        d = now().strftime("%Y%m%d")
        return "emails/{}/{}/{}/".format(d, instance.email.pk, filename)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.ForeignKey(EmailCollection, on_delete=models.CASCADE)
    location = models.FileField(upload_to=get_upload_location)

    def __str__(self):
        return str(self.email.email_from)
