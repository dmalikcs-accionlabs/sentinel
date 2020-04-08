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
            c.apply_async(self.pk)

    @property
    def body(self):
        #  todo: update form json
        return "return body from json file"

    @property
    def email_to(self):
        # todo: update  from json
        return "dmalikcs@gmail.com"

    @property
    def attachments(self):
        ## todo: update from JSON
        return "attachemnts"

    @property
    def email_date(self):
        ## todo: update from JSON
        return self.created_at

    def publish_order(self, order_id):
        connection_str = \
            'Endpoint=sb://dynastydev.servicebus.windows.net/;SharedAccessKeyName=CancelledOrders;SharedAccessKey=QyZ7PCAb3ofM4UbQMux0LFy0otDh0PqqDy33DthoaLU='
        sb_client = ServiceBusClient.from_connection_string(connection_str)
        queue_client = sb_client.get_queue("CancelledOrders")
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
