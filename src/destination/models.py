from django.db import models
from utils.models import BaseTimeStampField


class DestinationQueue(BaseTimeStampField):
    queue = models.CharField(verbose_name="queue name", max_length=75)
    desc = models.TextField(editable=False, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('queue', 'is_active',)
        verbose_name = 'queue'
        verbose_name_plural = 'queues'

    def __str__(self):
        return self.queue

    def publish(self, meta):
        pass