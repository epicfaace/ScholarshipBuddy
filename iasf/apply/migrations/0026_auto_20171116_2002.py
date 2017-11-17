# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-17 04:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apply', '0025_applicationinprogress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
