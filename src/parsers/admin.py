# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Template, Subject


class SubjectInlineAdmin(admin.TabularInline):
    model = Subject
    list_display = (
        'id',
        'created_at',
        'updated',
        'deleted',
        'template',
        'title',
        'match_type',
    )


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    inlines = [SubjectInlineAdmin, ]
    list_display = (
        'id',
        'created_at',
        'updated',
        'deleted',
        'title',
        'user',
    )
    list_filter = ('created_at', 'updated', 'deleted', 'user')
    date_hierarchy = 'created_at'

