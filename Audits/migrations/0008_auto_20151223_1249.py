# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Audits', '0007_auto_20151214_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='create_user',
            field=models.ForeignKey(related_name='create_tags', default='2', verbose_name='Creator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='public',
            field=models.BooleanField(default='2', verbose_name='Public'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='result',
            name='item',
            field=models.ForeignKey(related_name='results', to='Audits.Item'),
        ),
    ]
