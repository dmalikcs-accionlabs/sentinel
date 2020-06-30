from django.db import models
from utils.models import BaseTimeStampField
from django.conf import settings
from azure.servicebus import QueueClient, Message, ServiceBusClient
from django.core.serializers.json import DjangoJSONEncoder
import json
from collector.models import SBEmailParsing, EmailCollection, PDFCollection, \
    PDFData


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
        if not settings.AZURE_SB_CONN_STRING:
            print("Azure service bus in not configured properly")
            return
        connection_str = settings.AZURE_SB_CONN_STRING
        sb_client = QueueClient.from_connection_string(connection_str, self.queue)
        queue_client = sb_client
        if isinstance(email, PDFCollection):
            pages = PDFData.objects.filter(pdf=email)
            content = dict()
            ticket_list = list()
            for page in pages:
                if page.meta:
                    ticket = {key: value for key, value in page.meta.items()} if page.meta else dict()
                    ticket_list.append(ticket)

            content['clientId'] = email.client_id
            content['fromEmail'] = email.from_address
            content['toEmail'] = email.to_addresses
            content['ticket'] = ticket_list

        else:
            content = {key: value for key, value in email.meta.items()} if email.meta else dict()
            if isinstance(email, EmailCollection):
                pass
                content["SenderAddress"] = email.email_from
                content["EmailDate"] = email.email_date
            elif isinstance(email, SBEmailParsing):
                content['InboxUsername'] = email.inbox_username
                content['ClientID'] = email.client_id
                content["SenderAddress"] = email.from_address
                content["EmailDate"] = email.created_at
        queue_client.send(Message(json.dumps({
            "CreationDate": email.created_at,
            "MessageType": 0,
            "Content": content
        }, cls=DjangoJSONEncoder), ))
