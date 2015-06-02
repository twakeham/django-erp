# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basefield',
            name='verbose_name',
            field=models.CharField(max_length=64, verbose_name=b'Caption', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='field',
            name='type',
            field=models.IntegerField(choices=[(1, 'Short Text'), (2, 'Text'), (3, 'Slug'), (4, 'Email'), (5, 'URL'), (6, 'Boolean'), (7, 'Integer'), (8, 'Big Integer'), (9, 'Float'), (10, 'Decimal'), (11, 'Date'), (12, 'Time'), (13, 'Date/Time'), (14, 'File'), (15, 'Image'), (16, 'User')]),
            preserve_default=True,
        ),
    ]
