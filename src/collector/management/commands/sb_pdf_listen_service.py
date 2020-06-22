import json
from django.core.management.base import BaseCommand
from azure.servicebus import QueueClient, Message, ServiceBusClient
from collector.serializer import  PDFCollectionSerilizers
from collector.models import PDFData

import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
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
                    pdfFile = wi(filename=path, resolution=500)
                    image = pdfFile.convert('jpeg')
                    imageBlobs = []
                    for img in image.sequence:
                        imgPage = wi(image=img)
                        imageBlobs.append(imgPage.make_blob('jpeg'))
                    data['number_of_pages'] = len(imageBlobs)
                    p = PDFCollectionSerilizers(data=data)
                    if p.is_valid():
                        obj = p.save()

                        i = 1
                        for imgBlob in imageBlobs:
                            image = Image.open(io.BytesIO(imgBlob))
                            text = pytesseract.image_to_string(image, lang='eng')
                            pdf_data = {
                                'pdf': obj,
                                'content': text,
                                'page_number': i
                            }
                            PDFData.objects.create(**pdf_data)
                            i += 1
                        obj.initiate_async_parser()
                        message.complete()
