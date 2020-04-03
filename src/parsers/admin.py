# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Template, Subject, ParsingTask


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


@admin.register(ParsingTask)
class ParsingTaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated',
        'deleted',
        'parser',
        'desc',
    )
    list_filter = ('created_at', 'updated', 'deleted')
    date_hierarchy = 'created_at'