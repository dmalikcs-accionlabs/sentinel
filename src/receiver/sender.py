from azure.servicebus import QueueClient, Message, ServiceBusClient
from django.core.serializers.json import DjangoJSONEncoder
import json

connection_str = \
    'Endpoint=sb://dynastydev.servicebus.windows.net/;SharedAccessKeyName=read-write;SharedAccessKey=t7Yp6rbqvtHZDT9DYY5ud87PRoHNlyOUuTOJGzmiXek='
# sb_client = ServiceBusClient.from_connection_string(connection_str)
queue_client = QueueClient.from_connection_string(connection_str, "apemailparserequest")
queue_client.send(Message(json.dumps({
    # "CreationDate": e.created_at,
    "MessageType": 0,
    "Content": {
        "ClientId": 2,
        "UniqueIdentifier": "uid-111",
        "InboxUsername": "dmalikcs",
        "Subject": "Order #9898",
        "BodyPlainText": "Normal body",
        "BodyHtmlContent": "This is HTML body",
        "FromAddress": "dmalikcs@gmail.com",
        "ToAddresses": "dmalikcs@gmail.com",
    }
}), ))
