# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 20:02
from __future__ import unicode_literals

from django.db import migrations
import iasf.apply.fields


class Migration(migrations.Migration):

    dependencies = [
        ('apply', '0010_application_scores_ap'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='activities',
            field=iasf.apply.fields.ActivitiesField(blank=True, null=True),
        ),
    ]
