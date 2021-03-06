# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 02:21
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_home', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Home Phone')),
                ('phone_mobile', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Mobile Phone')),
                ('parent_first_name', models.CharField(max_length=50)),
                ('parent_middle_name', models.CharField(max_length=50)),
                ('parent_last_name', models.CharField(max_length=50)),
                ('claim_indian_maternal', models.BooleanField(verbose_name='Claim to Indian descent via maternal grandparents')),
                ('claim_indian_paternal', models.BooleanField(verbose_name='Claim to Indian descent via paternal grandparents')),
                ('high_school', models.CharField(max_length=100)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
