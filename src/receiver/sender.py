from azure.servicebus import QueueClient, Message, ServiceBusClient
from django.core.serializers.json import DjangoJSONEncoder
import json

connection_str = \
    'Endpoint=sb://dynastydev.servicebus.windows.net/;SharedAccessKeyName=CancelledOrders;SharedAccessKey=QyZ7PCAb3ofM4UbQMux0LFy0otDh0PqqDy33DthoaLU='
sb_client = ServiceBusClient.from_connection_string(connection_str)
queue_client = sb_client.get_queue("CancelledOrders")
queue_client.send(Message(json.dumps({
    # "CreationDate": e.created_at,
    "MessageType": 0,
    "Content": {
        "SenderAddress": 'dmalicks@gmail.com',
        # "EmailDate": e.email_date,
        "OrderNumber": '122'
    }
}), ))
