# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-20 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Audits', '0012_auto_20160203_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='question',
            field=models.TextField(verbose_name='Question'),
        ),
    ]
