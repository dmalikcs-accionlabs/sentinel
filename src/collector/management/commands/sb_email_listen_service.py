import json

from django.core.management.base import BaseCommand
from azure.servicebus import QueueClient, Message, ServiceBusClient
from collector.serializer import SBEmailParsingSerilizers


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        parser.add_argument('--verbose', type=int, nargs='?', default=0)

    def handle(self, *args, **options):
        is_verbose = options.get('verbose')
        AP_EMAIL_PARSING_QUEUE = 'apemailparserequest'
        connection_str = \
            'Endpoint=sb://dynastydev.servicebus.windows.net/;SharedAccessKeyName=read-write;SharedAccessKey=t7Yp6rbqvtHZDT9DYY5ud87PRoHNlyOUuTOJGzmiXek='

        sb_client = QueueClient.from_connection_string(connection_str, AP_EMAIL_PARSING_QUEUE)
        if is_verbose: print("Starting service bus listening services on queue {}".format(AP_EMAIL_PARSING_QUEUE))
        with sb_client.get_receiver() as messages:
            for message in messages:
                if is_verbose: print(message)
                m = next(message.body)
                d = json.loads(m)['Content']
                s = SBEmailParsingSerilizers(data=d)
                if s.is_valid():
                    s.save()
                message.complete()