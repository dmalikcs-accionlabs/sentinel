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
from sentinel.models import AppToken
from django.http import HttpResponseForbidden

logger = logging.getLogger('sentinel')


class ReadEmailView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        try:
            AppToken.objects.get(pk=kwargs['token'])
        except AppToken.DoesNotExist:
            return HttpResponseForbidden("Application doesn't have permission to send webhook")
        emailmsg = dict(request.POST)
        envelop_dict = dict(json.loads(emailmsg.get('envelope')[0]))
        required_data = {
                "subject": emailmsg.get('subject')[0],
                "email_from": envelop_dict.get('from'),
                "email_to": envelop_dict.get('to')[0],
            }
        received_email = EmailCollection.objects.create(**required_data)
        received_email.location.save("{}.json".format(received_email.pk), ContentFile(json.dumps(request.POST).encode('utf-8')))
        received_email.initiate_async_parser()
        if int(emailmsg.get('attachments')[0]) > 0:
            for key, val in request.FILES.items():
                email_attachment = EmailAttachment.objects.create(email=received_email)
                email_attachment.location.save(val.name, ContentFile(val.read()))
            print("Files saved successfully")
        log_fields = get_email_log_variable(received_email)
        logger.info(
            msg="Received Email from {}".format(required_data['email_from']),
            extra=log_fields)
        return Response("Ok", status=status.HTTP_200_OK)


