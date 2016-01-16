# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Audits', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='value',
            field=models.DecimalField(verbose_name='Value', max_digits=3, decimal_places=2),
        ),
    ]
