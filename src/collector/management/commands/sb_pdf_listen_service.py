import json
from django.core.management.base import BaseCommand
from azure.servicebus import QueueClient, Message, ServiceBusClient
from collector.serializer import SBEmailParsingSerilizers, PDFCollectionSerilizers
from collector.models import PDFData
from PyPDF2 import PdfFileReader
from django.conf import settings

class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        parser.add_argument('--verbose', type=int, nargs='?', default=0)

    def handle(self, *args, **options):
        is_verbose = options.get('verbose')
        SENTINEL_AP_PDF_PARSING_QUEUE_NAME = settings.SENTINEL_AP_PDF_PARSING_QUEUE_NAME
        SENTINEL_PDF_PARSING_SB_CONNECTION_STRING = settings.SENTINEL_PDF_PARSING_SB_CONNECTION_STRING

        sb_client = QueueClient.from_connection_string(SENTINEL_PDF_PARSING_SB_CONNECTION_STRING, SENTINEL_AP_PDF_PARSING_QUEUE_NAME)
        if is_verbose: print("Starting service bus listening services on queue {}".format(SENTINEL_AP_PDF_PARSING_QUEUE_NAME))
        with sb_client.get_receiver() as messages:
            for message in messages:
                if is_verbose: print(message)
                m = next(message.body)
                data = json.loads(m)['Content']
                if data.get('pdfLink'):
                    path = data.get('pdfLink')
                    with open(path, 'rb') as f:
                        pdf_obj = PdfFileReader(f)
                        data['number_of_pages'] = pdf_obj.numPages
                        print("########",data)
                        p = PDFCollectionSerilizers(data=data)
                        if p.is_valid():
                            obj = p.save()
                        print("$$$$",p.errors)
                        print("########", obj.id)
                        i = 0
                        while i < data['number_of_pages']:
                            page_obj = pdf_obj.getPage(i)
                            pdf_data = {
                                'pdf': obj,
                                'content': page_obj.extractText(),
                                'page_number': i + 1
                            }
                            PDFData.objects.create(**pdf_data)
                            i += 1
                        obj.initiate_async_parser()
                        message.complete()
