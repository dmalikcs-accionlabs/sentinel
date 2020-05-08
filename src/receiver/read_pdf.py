
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentinel.settings')
django.setup()

from collector.models import PDFCollection, PDFData
from PyPDF2 import PdfFileReader
from azure.servicebus import QueueClient, Message, ServiceBusClient
from django.conf import settings


def read_pdf(path):
    with open(path, 'rb') as f:
        pdf_obj = PdfFileReader(f)
        num_of_pages = pdf_obj.numPages
        required_data = {
            'location': path,
            'number_of_pages':num_of_pages
        }
        pdf = PDFCollection.objects.create(**required_data)
        i=0
        while i < num_of_pages:
            page_obj = pdf_obj.getPage(i)
            data = {
                'pdf':pdf,
                'content' : page_obj.extractText(),
                'page_number' : i+1
            }
            PDFData.objects.create(**data)
            i += 1


connection_str = \
    'Endpoint=sb://dynastydev.servicebus.windows.net/;SharedAccessKeyName=CancelledOrders;SharedAccessKey=QyZ7PCAb3ofM4UbQMux0LFy0otDh0PqqDy33DthoaLU='
sb_client = QueueClient.from_connection_string(connection_str, "cancelledorders")


with sb_client.get_receiver() as messages:
    for message in messages:
        data = json.loads(str(message))
        content = data.get('Content')
        if content.get('path'):
            read_pdf(content.get('path'))
        message.complete()


