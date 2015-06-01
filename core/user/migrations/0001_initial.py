# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoUserField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.OneToOneField(related_name='autouserfield', to='dynamic.Field')),
            ],
            options={
                'verbose_name': 'Authenticated user field',
            },
            bases=(models.Model,),
        ),
    ]
