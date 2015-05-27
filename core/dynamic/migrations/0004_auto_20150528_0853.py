# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic', '0003_auto_20150527_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='type',
            field=models.IntegerField(choices=[(5, b'Short Text'), (18, b'Text'), (16, b'Slug'), (9, b'Email'), (20, b'URL'), (4, b'Boolean'), (14, b'Integer'), (2, b'Big Integer'), (12, b'Float'), (8, b'Decimal'), (6, b'Date'), (19, b'Time'), (7, b'Date/Time'), (10, b'File'), (13, b'Image')]),
            preserve_default=True,
        ),
    ]
