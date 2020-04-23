from django.db import models
from utils.models import BaseTimeStampField
from django.conf import settings
from azure.servicebus import QueueClient, Message, ServiceBusClient
from django.core.serializers.json import DjangoJSONEncoder
import json


class DestinationQueue(BaseTimeStampField):
    queue = models.CharField(verbose_name="queue name", max_length=75)
    desc = models.TextField(editable=False, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('queue', 'is_active',)
        verbose_name = 'queue'
        verbose_name_plural = 'queues'

    def __str__(self):
        return self.queue

    def publish(self, email, kwargs=None):
        print(settings.AZURE_SB_CONN_STRING)
        if not settings.AZURE_SB_CONN_STRING:
            print("Azure service bus in not configured properly")
            return
        connection_str = settings.AZURE_SB_CONN_STRING
        sb_client = ServiceBusClient.from_connection_string(connection_str)
        queue_client = sb_client.get_queue(self.queue)
        content = {key: value for key, value in email.items()} if email.meta else dict()
        content["SenderAddress"] = email.email_from
        content["EmailDate"] = email.email_date
        queue_client.send(Message(json.dumps({
            "CreationDate": email.created_at,
            "MessageType": 0,
            "Content": content
        }, cls=DjangoJSONEncoder), ))
