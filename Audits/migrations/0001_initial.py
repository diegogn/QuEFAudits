# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import oauth2client.django_orm
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(default=b'a@f.esa', max_length=254)),
                ('name', models.CharField(max_length=b'50', verbose_name='Name')),
                ('surname', models.CharField(max_length=b'50', verbose_name='Surname')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('value', models.TextField(verbose_name='Value')),
            ],
        ),
        migrations.CreateModel(
            name='Audit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('creationDate', models.DateField(verbose_name='CreationDate')),
                ('startDate', models.DateField(verbose_name='StartDate')),
                ('eventId', models.IntegerField(null=True)),
                ('regularityInt', models.IntegerField(verbose_name='Regularity')),
                ('regularity', models.CharField(max_length=100, verbose_name='Period', choices=[(b'DAYLY', 'DAYLY'), (b'WEAKLY', 'WEAKLY'), (b'MONTHLY', 'MONTHLY'), (b'YEARLY', 'YEARLY')])),
            ],
        ),
        migrations.CreateModel(
            name='Auditor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(default=b'a@f.esa', max_length=254)),
                ('name', models.CharField(max_length=b'50', verbose_name='Name')),
                ('surname', models.CharField(max_length=b'50', verbose_name='Surname')),
            ],
        ),
        migrations.CreateModel(
            name='CredentialsModel',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('credential', oauth2client.django_orm.CredentialsField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=100, verbose_name='Filename')),
                ('docFile', models.FileField(upload_to=b'Documents/%Y%m%d', verbose_name='File')),
            ],
        ),
        migrations.CreateModel(
            name='Gestor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(default=b'a@f.esa', max_length=254)),
                ('name', models.CharField(max_length=b'50', verbose_name='Name')),
                ('surname', models.CharField(max_length=b'50', verbose_name='Surname')),
            ],
        ),
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Date', models.DateField(verbose_name='Date')),
                ('audit', models.ForeignKey(to='Audits.Audit')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('question', models.CharField(max_length=100, verbose_name='Question')),
                ('url', models.URLField(verbose_name='URL', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.ForeignKey(to='Audits.Answer', null=True)),
                ('instance', models.ForeignKey(to='Audits.Instance')),
                ('item', models.ForeignKey(to='Audits.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', verbose_name='Father Tag', blank=True, to='Audits.Tag', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(default=b'a@f.esa', max_length=254)),
                ('name', models.CharField(max_length=b'50', verbose_name='Name')),
                ('surname', models.CharField(max_length=b'50', verbose_name='Surname')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='tag',
            field=models.ForeignKey(verbose_name='Tag', to='Audits.Tag'),
        ),
        migrations.AddField(
            model_name='instance',
            name='items',
            field=models.ManyToManyField(to='Audits.Item', verbose_name='Items', through='Audits.Result'),
        ),
        migrations.AddField(
            model_name='document',
            name='instance',
            field=models.ForeignKey(to='Audits.Instance', null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='item',
            field=models.ForeignKey(to='Audits.Item', null=True),
        ),
        migrations.AddField(
            model_name='audit',
            name='auditor',
            field=models.ForeignKey(related_name='auditor', verbose_name='Auditor', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='audit',
            name='gestor',
            field=models.ForeignKey(related_name='gestor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='audit',
            name='tags',
            field=models.ManyToManyField(to='Audits.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='audit',
            name='usuario',
            field=models.ForeignKey(related_name='usuario', verbose_name='User', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='item',
            field=models.ForeignKey(to='Audits.Item'),
        ),
    ]
