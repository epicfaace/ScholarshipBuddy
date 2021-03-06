# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 22:16
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apply', '0007_auto_20171025_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='college_costs_applicant',
            field=models.IntegerField(blank=True, null=True, verbose_name='Approximate college cost for applicant'),
        ),
        migrations.AddField(
            model_name='application',
            name='college_costs_dependents',
            field=models.IntegerField(blank=True, null=True, verbose_name='Approximate college cost for other dependents'),
        ),
        migrations.AddField(
            model_name='application',
            name='financial_needs_statement',
            field=models.TextField(blank=True, null=True, verbose_name='Please describe any unusual financial circumstances in your family not listed previously on your application. You may include any information that will be beneficial to the Indian American Scholarship committee. Attach separately, if needed.'),
        ),
        migrations.AddField(
            model_name='application',
            name='income_parent',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='income_student',
            field=models.IntegerField(blank=True, null=True, verbose_name='Expected financial contribution'),
        ),
        migrations.AddField(
            model_name='application',
            name='scholarships_hope',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='scholarships_other',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='scholarships_pell',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='home_zip_code',
            field=models.CharField(blank=True, default='', max_length=5, verbose_name='Zip Code'),
        ),
        migrations.AlterField(
            model_name='application',
            name='hs_zip_code',
            field=models.CharField(blank=True, default='', max_length=5, verbose_name='Zip Code'),
        ),
        migrations.AlterField(
            model_name='application',
            name='list_dependents',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='List of dependents currently entering college'),
        ),
        migrations.AlterField(
            model_name='application',
            name='scores_ap',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
