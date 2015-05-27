# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldRegistryData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='field',
            name='type',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
