# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Audits', '0002_auto_20151203_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='weight',
            field=models.DecimalField(default=1.0, verbose_name='Weight', max_digits=3, decimal_places=2),
            preserve_default=False,
        ),
    ]
