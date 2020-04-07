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


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    inlines = [SubjectInlineAdmin, ]
    list_display = (
        'id',
        'title',
        'created_at',
    )
    list_filter = ('created_at', 'updated', 'deleted', 'user')
    date_hierarchy = 'created_at'


@admin.register(ParsingTask)
class ParsingTaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'parser',
        'desc',
        'created_at'
    )
    list_filter = ('created_at', 'updated', 'deleted')
    date_hierarchy = 'created_at'