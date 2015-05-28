# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic', '0001_initial'),
        ('form', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('model_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dynamic.Model')),
                ('require_id', models.BooleanField(default=True, help_text=b'Require user to login prior to completing checklist.')),
                ('datestamp', models.BooleanField(default=True, help_text=b'Date stamp all entries.')),
                ('followup_form', models.ForeignKey(related_name='followup_forms', blank=True, to='form.ModelForm', help_text=b'Form to be filled out prior to completing checklist.', null=True, verbose_name=b'Followup form')),
                ('form', models.ForeignKey(related_name='preforms', blank=True, to='form.ModelForm', help_text=b'Form to be filled out prior to completing checklist.', null=True, verbose_name=b'Form')),
            ],
            options={
            },
            bases=('dynamic.model',),
        ),
        migrations.CreateModel(
            name='ChecklistItemComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_object_id', models.PositiveIntegerField()),
                ('record_object_id', models.PositiveIntegerField()),
                ('comment', models.TextField(null=True, blank=True)),
                ('field_content_type', models.ForeignKey(related_name='checkfield', to='contenttypes.ContentType')),
                ('record_content_type', models.ForeignKey(related_name='checkrecord', to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
