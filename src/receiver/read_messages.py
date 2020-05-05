from azure.servicebus import QueueClient, Message, ServiceBusClient

connection_str = \
    'Endpoint=sb://dynastydev.servicebus.windows.net/;SharedAccessKeyName=CancelledOrders;SharedAccessKey=QyZ7PCAb3ofM4UbQMux0LFy0otDh0PqqDy33DthoaLU='
# sb_client = ServiceBusClient.from_connection_string(connection_str)
sb_client = QueueClient.from_connection_string(connection_str, "cancelledorders")

with sb_client.get_receiver() as messages:
    for message in messages:
        print(message)
        message.complete()