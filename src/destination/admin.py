# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import DestinationQueue


@admin.register(DestinationQueue)
class DestinationQueueAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'queue',
        'is_active',
        'created_at',
    )
    list_filter = ('created_at', 'updated', 'deleted', 'is_active')
    date_hierarchy = 'created_at'
