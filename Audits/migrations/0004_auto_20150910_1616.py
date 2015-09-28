# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Audits', '0003_auto_20150810_1933'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='fatherTag',
            new_name='father_tag',
        ),
        migrations.AlterField(
            model_name='audit',
            name='auditor',
            field=models.ForeignKey(related_name='auditor', verbose_name='Auditor', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='audit',
            name='gestor',
            field=models.ForeignKey(related_name='gestor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='audit',
            name='usuario',
            field=models.ForeignKey(related_name='usuario', verbose_name='User', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
