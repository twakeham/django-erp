# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic', '0002_auto_20150601_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relation',
            name='type',
            field=models.IntegerField(choices=[(30, b'Foreign Key'), (31, b'Many to Many'), (32, b'One to One'), (33, b'Generic Relation')]),
            preserve_default=True,
        ),
    ]
