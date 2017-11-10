# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Application

class ApplicationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Application, ApplicationAdmin)