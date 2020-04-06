from django.db import models

from django.contrib.auth import get_user_model
from django.utils.decorators import classonlymethod
from parsers.models import BaseTimeStampField
User =  get_user_model()


class EmailData(BaseTimeStampField):
    to_email_id = models.CharField(max_length=250)
    from_email_id = models.CharField(max_length=250)
    email_envelope = models.TextField(blank=True)
    subject = models.TextField(blank=True)
    body = models.TextField(null=True, blank=True)
    email_date = models.DateTimeField(auto_now=True)



