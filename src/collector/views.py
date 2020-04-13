from django.shortcuts import render
from rest_framework.views import APIView
import simplejson
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status

from django.core.files.base import ContentFile
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from collector.models import EmailCollection, EmailAttachment
from django.utils.timezone import now
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from custom_logging.custom_logging import get_email_log_variable
from custom_logging.choices import EMAILLoggingChoiceField
import logging

logger = logging.getLogger('sentinel')

#
# class EmailSerializer:
#     def __init__(self, req):
#         self.req = req
#
#         self.base_email_parser(self.req.POST, self.req.FILES)
#
#     def base_email_parser(self, req, filedict=None):
#         print(json.dumps(req.POST))
#         mail = {}
#         errors = {}
#         if req is None:
#             return None
#
#         if getattr(req, 'method', None) is None:
#             return None
#
#         if getattr(req, 'form', None) is None:
#             return None
#
#         if req.method != 'POST':
#             return None
#
#         if req.form is None:
#             return None
#
#         if req is None:
#             return None
#         mail['cc'] = self.req.get('cc', None)
#         mail['bcc'] = self.req.get('bcc', None)
#         mail['text'] = self.req.get('text', None)
#         mail['html'] = self.req.get('html', None)
#         mail['envelope'] = self.req.get('envelope', None)
#         ##check for attachments
#         mail['attachments'] = []
#         mail['attachment-info'] = self.req.get('attachment-request', None)
#         no_attachments = int(self.req.get('attachments', 0))
#
#         if no_attachments > 0:
#             if filedict is None:
#                 errors['attachments'] = "file dictionary is empty / None."
#                 for no in range(1, no_attachments + 1):
#                     attachment = 'attachment%d' % no
#                     mail['attachments'].append(attachment)
#             # If the attachment is available,
#             # append the file objects instead.
#             else:
#                 for no in range(1, no_attachments + 1):
#                     attachment = filedict.get('attachment%d' % no, None)
#                     if attachment is None:
#                         errors['attachment%d' % no] = "attachment%d is empty." % no
#                     else:
#                         mail['attachments'].append(attachment)
#
#         print(mail)
#         print("$$$$$$$$$$$$$$$$$$$$$$$$")
#         print(errors)


class ReadEmailView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        emailmsg = dict(request.POST)
        envelop_dict = dict(json.loads(emailmsg.get('envelope')[0]))
        required_data = {
                "subject": emailmsg.get('subject')[0],
                "email_from": envelop_dict.get('from'),
            }
        received_email = EmailCollection.objects.create(**required_data)
        received_email.location.save("{}.json".format(received_email.pk), ContentFile(json.dumps(request.POST)))
        if int(emailmsg.get('attachments')[0]) > 0:
            for key, val in request.FILES.items():
                email_attachment = EmailAttachment.objects.create(email=received_email)
                email_attachment.location.save(val.name, ContentFile(val.read()))
            print("Files saved successfully")
        log_fields = get_email_log_variable(received_email)
        logger.info(
            msg="Recived Email from {}".format(required_data['email_from']),
            extra=log_fields)
        return Response("Ok", status=status.HTTP_200_OK)


