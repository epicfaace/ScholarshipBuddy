# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 03:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apply', '0004_auto_20171024_2034'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_1', models.CharField(max_length=128, verbose_name='address')),
                ('address_2', models.CharField(blank=True, max_length=128, verbose_name="address cont'd")),
                ('city', models.CharField(default='', max_length=64, verbose_name='city')),
                ('state', models.CharField(default='GA', max_length=2, verbose_name='state')),
                ('zip_code', models.CharField(default='', max_length=5, verbose_name='zip code')),
            ],
        ),
        migrations.RenameField(
            model_name='application',
            old_name='high_school',
            new_name='hs_name',
        ),
        migrations.AlterField(
            model_name='application',
            name='parent_middle_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='application',
            name='home_address',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_address', to='apply.Address'),
        ),
        migrations.AddField(
            model_name='application',
            name='hs_address',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hs_address', to='apply.Address'),
        ),
    ]
