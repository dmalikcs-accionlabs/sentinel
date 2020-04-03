from django.db import models
from utils.models import BaseTimeStampField
# Create your models here.
from django.utils.decorators import classonlymethod


class EmailBodyTypeChoice:
    HTML= 'h'
    TEXT = 'T'

    @classonlymethod
    def get_choices(cls):
        return (
            (cls.HTML, 'HTML'),
            (cls.TEXT, 'Text')
        )

EMAIL_BODY_TYPE_LIST = EmailBodyTypeChoice.get_choices()


class EmailCollection(BaseTimeStampField):
    location = models.FileField(upload_to='emails/', null=True, editable=False)
    email_from = models.EmailField()
    subject = models.CharField(max_length=256, blank=True)
    body = models.TextField(blank=True)
    body_type = models.CharField(max_length=1, choices=EMAIL_BODY_TYPE_LIST,
                                 default=EmailBodyTypeChoice.TEXT)

    class Meta:
        ordering = ('-created_at', )

    def save(self, *args,  **kwargs):
        created =  self._state.adding
        if created:
            pass
            # create a parser mataching logic & save data into blob storage
        super(EmailCollection, self).save(*args, **kwargs)


class EmailAttachment(BaseTimeStampField):
    email = models.ForeignKey(EmailCollection, on_delete=models.CASCADE)
    location = models.FileField(upload_to='email/attachments/')
