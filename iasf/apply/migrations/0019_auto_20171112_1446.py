# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 22:46
from __future__ import unicode_literals

from django.db import migrations
import iasf.apply.fields


class Migration(migrations.Migration):

    dependencies = [
        ('apply', '0018_auto_20171112_1429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='activities',
        ),
        migrations.AddField(
            model_name='application',
            name='activities_awards',
            field=iasf.apply.fields.JSONListSchemaField(blank=True, null=True, verbose_name='Academic awards / honors'),
        ),
        migrations.AddField(
            model_name='application',
            name='activities_extracurriculars',
            field=iasf.apply.fields.JSONListSchemaField(blank=True, null=True, verbose_name='Athletics / Clubs / Extracurriculars'),
        ),
        migrations.AddField(
            model_name='application',
            name='activities_other',
            field=iasf.apply.fields.JSONListSchemaField(blank=True, null=True, verbose_name='Other'),
        ),
        migrations.AddField(
            model_name='application',
            name='activities_workexperience',
            field=iasf.apply.fields.JSONListSchemaField(blank=True, null=True, verbose_name='Work Experience'),
        ),
        migrations.AlterField(
            model_name='application',
            name='finaid_list_dependents',
            field=iasf.apply.fields.JSONListSchemaField(blank=True, null=True, verbose_name='List of dependents currently entering college'),
        ),
    ]
