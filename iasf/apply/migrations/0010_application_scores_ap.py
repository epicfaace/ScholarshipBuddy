# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 18:19
from __future__ import unicode_literals

from django.db import migrations
import iasf.apply.fields


class Migration(migrations.Migration):

    dependencies = [
        ('apply', '0009_remove_application_scores_ap'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='scores_ap',
            field=iasf.apply.fields.ScoresAPField(blank=True, null=True),
        ),
    ]
