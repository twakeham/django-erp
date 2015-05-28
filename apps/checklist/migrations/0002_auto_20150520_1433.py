# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='followup_form',
            field=models.ForeignKey(related_name='followup_forms', blank=True, to='form.ModelForm', help_text=b'Form to be used for followup.', null=True, verbose_name=b'Followup form'),
            preserve_default=True,
        ),
    ]
