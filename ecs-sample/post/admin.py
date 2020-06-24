# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp', 'is_show']
    list_filter = ['is_show']
    list_editable = ['is_show']