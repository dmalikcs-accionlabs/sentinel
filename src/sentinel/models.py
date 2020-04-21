from django.db import models
import uuid
from utils.models import BaseTimeStampField


class AppToken(BaseTimeStampField):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=10)
