# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Audits', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='fatherTag',
            field=models.ForeignKey(related_name='children', verbose_name='Father Tag', to='Audits.Tag', null=True),
        ),
    ]
