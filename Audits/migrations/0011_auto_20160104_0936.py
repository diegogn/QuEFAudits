# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Audits', '0010_instance_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='obligatory',
        ),
        migrations.AddField(
            model_name='item',
            name='obligatory',
            field=models.CharField(default='SHALL', max_length=6, verbose_name='Obligatory', choices=[(b'SHALL', b'shall'), (b'SHOULD', b'should'), (b'MAY', b'may')]),
            preserve_default=False,
        ),
    ]
