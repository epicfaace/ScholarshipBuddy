# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 20:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apply', '0013_auto_20171102_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='file_resume',
            field=models.FileField(blank=True, null=True, upload_to=b''),
        ),
    ]
