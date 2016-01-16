# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Audits', '0003_tag_weight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audit',
            name='regularity',
        ),
        migrations.RemoveField(
            model_name='audit',
            name='regularityInt',
        ),
        migrations.AddField(
            model_name='audit',
            name='byday',
            field=models.CharField(max_length=100, null=True, verbose_name='Byday'),
        ),
        migrations.AddField(
            model_name='audit',
            name='bymonth',
            field=models.CharField(max_length=100, null=True, verbose_name='Bymonth'),
        ),
        migrations.AddField(
            model_name='audit',
            name='bymonthday',
            field=models.CharField(max_length=100, null=True, verbose_name='Bymonthday'),
        ),
        migrations.AddField(
            model_name='audit',
            name='bysetpos',
            field=models.IntegerField(null=True, verbose_name='Bysetpos'),
        ),
        migrations.AddField(
            model_name='audit',
            name='byyearday',
            field=models.CharField(max_length=800, null=True, verbose_name='Byyearday'),
        ),
        migrations.AddField(
            model_name='audit',
            name='count',
            field=models.IntegerField(null=True, verbose_name='Count'),
        ),
        migrations.AddField(
            model_name='audit',
            name='freq',
            field=models.CharField(max_length=100, null=True, verbose_name='Period', choices=[(b'DAYLY', 'Dayly'), (b'WEAKLY', 'Weakly'), (b'MONTHLY', 'Monthly'), (b'YEARLY', 'Yearly')]),
        ),
        migrations.AddField(
            model_name='audit',
            name='interval',
            field=models.IntegerField(null=True, verbose_name='Regularity'),
        ),
        migrations.AddField(
            model_name='audit',
            name='state',
            field=models.CharField(default='ACTIVE', max_length=100, verbose_name='State', choices=[(b'INACTIVE', 'Inactive'), (b'ACTIVE', 'Active'), (b'FINISH', 'Finish'), (b'ELIMINATED', 'Eliminated')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='audit',
            name='wkst',
            field=models.CharField(max_length=2, null=True, verbose_name='Wkst'),
        ),
    ]
