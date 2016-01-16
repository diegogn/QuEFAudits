# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Audits', '0008_auto_20151223_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='obligatory',
            field=models.CharField(default='SHALL', max_length=6, verbose_name='Obligatory', choices=[(b'SHALL', b'shall'), (b'SHOULD', b'should'), (b'MAY', b'may')]),
            preserve_default=False,
        ),
    ]
