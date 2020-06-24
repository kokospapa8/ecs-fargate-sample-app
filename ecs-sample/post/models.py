# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django_mysql.models import Model

User = get_user_model()

class Post(Model):
    title = models.CharField(max_length=128)
    body = models.TextField(blank=True, default="", help_text="HTML")
    timestamp = models.DateField(db_index=True, auto_now_add=True)
    is_show = models.BooleanField(default=False, db_index=True)
    link = models.URLField(blank=True, default="")
    user = models.ForeignKey(User, related_name="post_user", on_delete=models.PROTECT)

    class Meta:
        app_label = "post"
        db_table = "post_post"

