# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import AppToken


@admin.register(AppToken)
class AppTokenAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated', 'deleted', 'id', 'title')
    list_filter = ('created_at', 'updated', 'deleted')
    date_hierarchy = 'created_at'
