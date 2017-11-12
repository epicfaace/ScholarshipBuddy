# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 20:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apply', '0016_auto_20171112_1121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='college_costs_applicant',
            new_name='finaid_college_costs_applicant',
        ),
        migrations.RenameField(
            model_name='application',
            old_name='college_costs_dependents',
            new_name='finaid_college_costs_dependents',
        ),
        migrations.RenameField(
            model_name='application',
            old_name='income_student',
            new_name='finaid_expected_contribution',
        ),
        migrations.RenameField(
            model_name='application',
            old_name='income_parent',
            new_name='finaid_income_parent',
        ),
        migrations.RenameField(
            model_name='application',
            old_name='list_dependents',
            new_name='finaid_list_dependents',
        ),
        migrations.AddField(
            model_name='application',
            name='finaid_income_student',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
