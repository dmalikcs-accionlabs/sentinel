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

    def has_add_permission(self, request):
        if request.user and request.user.is_superuser:
            return True
        else:
            return False

    def get_queryset(self, request):
        return self.model.objects.filter(deleted__isnull=True)

@admin.register(EmailCollection)
class EmailCollectionAdmin(admin.ModelAdmin):
    readonly_fields = ['body', 'email_date', 'cc',
                       'content_ids', 'charsets',
                       'attachments_count', 'spf', 'meta', ]
    fieldsets = (
        (None, {
            'fields': (
                'template_match_status',

                ('email_from', 'subject'),
                ('cc', 'email_date', ),
                'body',
                ('content_ids', 'charsets', 'attachments_count', 'spf',),
                'meta'
            )
        }),

        # ('Advance content', {
        #     'classes': ('collapse',),
        #     'fields': (
        #         ('content_ids', 'charsets', 'attachments_count', 'spf', ),
        #     ),
        # }),


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
        'subject',
        'template',
        'is_published',
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

