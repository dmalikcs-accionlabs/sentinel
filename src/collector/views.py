from django.shortcuts import render
from rest_framework.views import APIView
import simplejson
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
import json
import uuid
from .serializers import EmailDataSerializer
from parsers.models import Subject,Template
class EmailSerializer:
    def __init__(self,req):
        self.req=req

        self.base_email_parser(self.req.POST, self.req.FILES)

    def base_email_parser(self,req, filedict=None):
        print(json.dumps(req.POST))
        mail ={}
        errors={}
        if req is None:
            return None

        if getattr(req, 'method', None) is None:
            return None

        if getattr(req, 'form', None) is None:
            return None

        if req.method != 'POST':
            return None

        if req.form is None:
            return None

        if req is None:
            return None
        mail['cc'] = self.req.get('cc', None)
        mail['bcc'] = self.req.get('bcc', None)
        mail['text'] = self.req.get('text', None)
        mail['html'] = self.req.get('html', None)
        mail['envelope'] = self.req.get('envelope', None)
        ##check for attachments
        mail['attachments'] = []
        mail['attachment-info'] = self.req.get('attachment-request', None)
        no_attachments = int(self.req.get('attachments', 0))

        if no_attachments > 0:
            if filedict is None:
                errors['attachments'] = "file dictionary is empty / None."
                for no in range(1, no_attachments + 1):
                    attachment = 'attachment%d' % no
                    mail['attachments'].append(attachment)
            # If the attachment is available,
            # append the file objects instead.
            else:
                for no in range(1, no_attachments + 1):
                    attachment = filedict.get('attachment%d' % no, None)
                    if attachment is None:
                        errors['attachment%d' % no] = "attachment%d is empty." % no
                    else:
                        mail['attachments'].append(attachment)

        print(mail)
        print("$$$$$$$$$$$$$$$$$$$$$$$$")
        print(errors)


import pprint


class ReadEmailView(APIView):
    def post(self, request):
        email_dict = request.POST.items()
        print(type(email_dict))
        # print(request.POST)
        # print("************************************************************")
        # print(request.data)
        required_data={}
        required_fields = ['to', 'from', 'envelope', 'subject', 'text','email']
        for key,val in email_dict:
            if key in required_fields:
                required_data[key] = val
                print("Key {} \t -> Val {}".format(key,val))
        filename = str(uuid.uuid4())
        with open(filename, 'w') as f:
            print(json.dumps(required_data), file=f)
        print("Email is saved to the file ".format(filename))
        serializer = EmailDataSerializer(data=required_data)  #(data=json.dumps(required_data)) ##error at this point
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestReadEmail(APIView):
    def get(self,request,*args,**kwargs):
        print("Hello")
        return HttpResponse("Hello")