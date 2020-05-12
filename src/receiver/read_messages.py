from azure.servicebus import QueueClient, Message, ServiceBusClient

connection_str = \
    'Endpoint=sb://dynastydev.servicebus.windows.net/;SharedAccessKeyName=read-write;SharedAccessKey=t7Yp6rbqvtHZDT9DYY5ud87PRoHNlyOUuTOJGzmiXek='
# sb_client = ServiceBusClient.from_connection_string(connection_str)
sb_client = QueueClient.from_connection_string(connection_str, "apemailparserequest")

with sb_client.get_receiver() as messages:
    for message in messages:
        print(message)
        message.complete()