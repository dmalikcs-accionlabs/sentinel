from django.db import models

class BaseTimeStampField(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(editable=False, null=True)

    class Meta:
        abstract = True