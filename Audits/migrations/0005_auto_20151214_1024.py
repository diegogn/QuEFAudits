# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Audits', '0004_auto_20151209_1013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='instance',
            old_name='Date',
            new_name='date',
        ),
        migrations.AddField(
            model_name='instance',
            name='level',
            field=models.CharField(default='LOW', max_length=6, verbose_name='Level', choices=[(b'LOW', 'Low'), (b'MEDIUM', 'Medium'), (b'HIGH', 'High')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instance',
            name='state',
            field=models.CharField(default='FINISHED', max_length=50, verbose_name='State', choices=[(b'STARTED', 'Started'), (b'FINISHED', 'Finished')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='audit',
            name='byday',
            field=models.CharField(max_length=100, null=True, verbose_name='Byday', blank=True),
        ),
        migrations.AlterField(
            model_name='audit',
            name='bymonth',
            field=models.CharField(max_length=100, null=True, verbose_name='Bymonth', blank=True),
        ),
        migrations.AlterField(
            model_name='audit',
            name='bymonthday',
            field=models.CharField(max_length=100, null=True, verbose_name='Bymonthday', blank=True),
        ),
        migrations.AlterField(
            model_name='audit',
            name='bysetpos',
            field=models.IntegerField(null=True, verbose_name='Bysetpos', blank=True),
        ),
        migrations.AlterField(
            model_name='audit',
            name='byyearday',
            field=models.CharField(max_length=800, null=True, verbose_name='Byyearday', blank=True),
        ),
        migrations.AlterField(
            model_name='audit',
            name='count',
            field=models.IntegerField(null=True, verbose_name='Count', blank=True),
        ),
        migrations.AlterField(
            model_name='audit',
            name='freq',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Period', choices=[(b'DAYLY', 'Dayly'), (b'WEAKLY', 'Weakly'), (b'MONTHLY', 'Monthly'), (b'YEARLY', 'Yearly')]),
        ),
        migrations.AlterField(
            model_name='audit',
            name='interval',
            field=models.IntegerField(null=True, verbose_name='Regularity', blank=True),
        ),
        migrations.AlterField(
            model_name='audit',
            name='wkst',
            field=models.CharField(max_length=2, null=True, verbose_name='Wkst', blank=True),
        ),
    ]
