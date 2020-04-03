# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Template, Subject


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
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


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated',
        'deleted',
        'template',
        'title',
        'match_type',
    )
    list_filter = ('created_at', 'updated', 'deleted', 'template')
    date_hierarchy = 'created_at'
