# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic', '0002_auto_20150527_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='type',
            field=models.IntegerField(choices=[(5, b'Short Text'), (18, b'Text'), (16, b'Slug')]),
            preserve_default=True,
        ),
    ]
