# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import EmailCollection, EmailAttachment


class EmailAttachmentInlineAdmin(admin.TabularInline):
    model = EmailAttachment
    list_display = (
        'id',
        'created_at',
        'updated',
        'deleted',
        'email',
        'location',
    )


@admin.register(EmailCollection)
class EmailCollectionAdmin(admin.ModelAdmin):
    inlines = [EmailAttachmentInlineAdmin, ]
    list_display = (
        'id',
        'created_at',
        'updated',
        'deleted',
        'location',
        'email_from',
        'subject',
        'is_published',
    )
    list_filter = ('created_at', 'updated', 'deleted', 'is_published')
    date_hierarchy = 'created_at'


