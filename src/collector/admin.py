# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import EmailCollection,\
    EmailAttachment, SBEmailParsing, PDFCollection, PDFData, \
    ParserExecutionHistory, PDFParserExecutionHistory


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


class ParserExecutionHistoryInlineAdmin(admin.TabularInline):
    model = ParserExecutionHistory
    readonly_fields = ['email', 'template',  'extracted_data', 'is_published']

    def has_add_permission(self, request):
        return False


@admin.register(EmailCollection)
class EmailCollectionAdmin(admin.ModelAdmin):
    readonly_fields = ['body', 'email_date', 'cc', 'email_from', 'subject',
                       'content_ids', 'charsets',
                       'attachments_count', 'spf', 'meta', 'email_to', 'template',]
    fieldsets = (
        (None, {
            'fields': (
                ('template_match_status', 'match_templates',),
                ('template'),
                ('email_from', 'subject', 'email_to'),
                'location',
                ('cc', 'email_date', ),
                'body',
                ('content_ids', 'charsets', 'attachments_count', 'spf',),
                'meta'
            )
        }),
    )
    search_fields = ['email_from', 'subject', 'email_to']
    inlines = [EmailAttachmentInlineAdmin, ParserExecutionHistoryInlineAdmin]
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

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)

        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False

        return formfield

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

class PDFDataInlineAdmin(admin.TabularInline):
    model = PDFData
    readonly_fields = ['content','page_number']
    list_display = (
        'id',
        'created_at',
        'updated',
        'deleted',
        'content',
        'page_number',
        'meta',
    )

    def has_add_permission(self, request):
        if request.user and request.user.is_superuser:
            return True
        else:
            return False

    def get_queryset(self, request):
        return self.model.objects.filter(deleted__isnull=True)


class PDFParserExecutionHistoryInlineAdmin(admin.TabularInline):
    model = PDFParserExecutionHistory
    readonly_fields = ['pdf', 'template',  'extracted_data', 'is_published']

    def has_add_permission(self, request):
        return False

@admin.register(PDFCollection)
class PDFCollectionAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'location', 'number_of_pages',
                       'from_address', 'to_addresses', 'client_id', 'type_id',
                       'template',]

    fieldsets = (
        (None, {
            'fields': (
                ('template_match_status', 'match_templates'),
                ('template'),
                ('from_address', 'to_addresses'),
                ('client_id','type_id'),
                ('location', 'number_of_pages'),
            )
        }),
    )
    list_display = (
        'id',
        'created_at',
        'updated',
        'deleted',
        'template',
        'is_published',
        'created_at',
    )

    list_filter = ('created_at', 'updated', 'deleted')
    date_hierarchy = 'created_at'
    inlines = [PDFDataInlineAdmin, PDFParserExecutionHistoryInlineAdmin]

    def has_add_permission(self, request):
        if request.user and request.user.is_superuser:
            return True
        else:
            return False

    def get_queryset(self, request):
        return self.model.objects.filter(deleted__isnull=True)

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)

        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False

        return formfield
