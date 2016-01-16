# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Audits', '0006_audit_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='audit',
            old_name='creationDate',
            new_name='creation_date',
        ),
        migrations.RenameField(
            model_name='audit',
            old_name='startDate',
            new_name='start_date',
        ),
    ]
