# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic', '0002_auto_20150601_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('dynamic.model',),
        ),
    ]
