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
    is_published = models.BooleanField(default=True, editable=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.email_from)

    @property
    def body(self):
        return "return body from json file"


    ## post save signal
    ## celery job e.==== template compare
    ##  ## parse attached
    ## parser run
    ### push into service  bus

    # def save(self, *args, **kwargs):
    #     created = self._state.adding
    #     if created:
    #         try:
    #             connection_str = \
    #                 'Endpoint=sb://dynastydev.servicebus.windows.net/;SharedAccessKeyName=CancelledOrders;SharedAccessKey=QyZ7PCAb3ofM4UbQMux0LFy0otDh0PqqDy33DthoaLU='
    #             sb_client = ServiceBusClient.from_connection_string(connection_str)
    #             queue_client = sb_client.get_queue("CancelledOrders")
    #             queue_client.send(Message(json.dumps( {
    #                 "CreationDate": "2020-04-03T13:12:32.6879998-03:00",
    #                 "MessageType": 0,
    #                 "Content": {
    #                     "SenderAddress": self.email_from,
    #                     "EmailDate": "2020-03-25T13:12:32.6887854-03:00",
    #                     "OrderNumber": "20255033"
    #                 }
    #             })))
    #         except Exception as e:
    #             print(e)
    #             self.is_published = False
    #         super(EmailCollection, self).save(*args, **kwargs)
    #

        # if created:
        #     self.location.save("{}.json".format(self.pk), ContentFile(json.dumps(
        #         {
        #             "CreationDate": "2020-04-03T13:12:32.6879998-03:00",
        #             "MessageType": 0,
        #             "Content": {
        #                 "SenderAddress": "vpedrosa@dynastyse.com",
        #                 "EmailDate": "2020-03-25T13:12:32.6887854-03:00",
        #                 "OrderNumber": "20255033"
        #             }
        #         }
        #     )))
        # @property
        # def email_date(self):
        #     return self.created_at


class EmailAttachment(BaseTimeStampField):
    def get_upload_location(instance, filename):
        d = now().strftime("%Y%m%d")
        return "emails/{}/{}/{}/".format(d, instance.email.pk, filename)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.ForeignKey(EmailCollection, on_delete=models.CASCADE)
    location = models.FileField(upload_to=get_upload_location)

    def __str__(self):
        return str(self.email.email_from)
