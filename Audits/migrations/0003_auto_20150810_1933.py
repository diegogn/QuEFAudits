# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Audits', '0002_auto_20150810_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='fatherTag',
            field=models.ForeignKey(related_name='children', verbose_name='Father Tag', blank=True, to='Audits.Tag', null=True),
        ),
    ]
