# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import EmailCollection,\
    EmailAttachment, SBEmailParsing


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

    def has_add_permission(self, request):
        if request.user and request.user.is_superuser:
            return True
        else:
            return False

    def get_queryset(self, request):
        return self.model.objects.filter(deleted__isnull=True)

@admin.register(EmailCollection)
class EmailCollectionAdmin(admin.ModelAdmin):
    readonly_fields = ['body', 'email_date', 'cc', 'email_from', 'subject',
                       'content_ids', 'charsets',
                       'attachments_count', 'spf', 'meta', 'email_to',]
    fieldsets = (
        (None, {
            'fields': (
                'template_match_status',
                ('email_from', 'subject', 'email_to'),
                'location',
                ('cc', 'email_date', ),
                'body',
                ('content_ids', 'charsets', 'attachments_count', 'spf',),
                'meta'
            )
        }),
        ('Template', {
            'classes': ('collapse',),
            'fields': (('template', ), ),
        }),
    )
    search_fields = ['email_from', 'subject', ]
    inlines = [EmailAttachmentInlineAdmin, ]
    list_display = (
        'id',
        'email_from',
        'email_to',
        'subject',
        'template',
        'is_published',
        'created_at',
    )
    list_filter = ('created_at', 'is_published')
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        if request.user and request.user.is_superuser:
            return True
        else:
            return False

    def get_queryset(self, request):
        return self.model.objects.filter(deleted__isnull=True)


@admin.register(SBEmailParsing)
class SBEmailParsingAdmin(admin.ModelAdmin):
    readonly_fields = ['body', 'body_plaintext', 'body_html_content', 'meta',]
    list_display = (
        'id',
        'client_id',
        'unique_identifier',
        'inbox_username',
        'subject',
        # 'body_plaintext',
        # 'body_html_content',
        'from_address',
        'to_addresses',
        'template',
        'is_published',
        'created_at',
    )
    fieldsets = (
        (None, {
            'fields': (
                'template_match_status',
                ('from_address', 'subject'),
                ('unique_identifier', 'inbox_username', ),
                'body_plaintext',
                'body_html_content',
                'meta'
            )
        }),
        ('Template', {
            'classes': ('collapse',),
            'fields': (('template', ), ),
        }),
    )

    list_filter = ('created_at', 'updated', 'deleted')
    date_hierarchy = 'created_at'

