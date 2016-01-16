# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Audits', '0005_auto_20151214_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='audit',
            name='description',
            field=models.TextField(verbose_name='Description', blank=True),
        ),
    ]
