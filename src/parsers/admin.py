# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Template, Subject, ParsingTask


class SubjectInlineAdmin(admin.TabularInline):
    model = Subject
    list_display = (
        'id',
        'template',
        'title',
        # 'match_type',
        'created_at',
    )


class ParsingTaskInlineAdmin(admin.TabularInline):
    model = ParsingTask
    list_display = (
        'id',
        'title',
        'parser',
        'regex',
        'desc',
        'created_at'
    )
    list_filter = ('created_at', 'updated', 'deleted')
    date_hierarchy = 'created_at'


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    inlines = [ParsingTaskInlineAdmin, ]
    search_fields = ['email_from', 'email_to', 'subject']
    fieldsets = (
        ('', {
            'fields': (
                'title',
                ('email_from', 'email_to',),
                'subject',
            ),
        }),
    )

    list_display = (
        'id',
        'title',
        'email_from',
        'email_to',
        'subject',
        'created_at',
    )
    list_filter = ('created_at', 'updated', 'deleted', 'user')
    date_hierarchy = 'created_at'

