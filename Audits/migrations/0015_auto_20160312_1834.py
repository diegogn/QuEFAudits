# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-12 17:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Audits', '0014_auto_20160312_1749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credentialsmodel',
            name='user',
        ),
        migrations.AddField(
            model_name='credentialsmodel',
            name='id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='credential', serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
