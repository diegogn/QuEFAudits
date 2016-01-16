# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Audits', '0009_answer_obligatory'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='tags',
            field=models.ManyToManyField(to='Audits.Tag', verbose_name='Tags'),
        ),
    ]
