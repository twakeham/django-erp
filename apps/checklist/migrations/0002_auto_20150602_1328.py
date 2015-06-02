# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic', '0002_auto_20150601_1405'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('checklist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChecklistFollowup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('photo', models.ImageField(upload_to=b'photo', blank=True)),
                ('signature', models.ImageField(upload_to=b'media', blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Checklist',
        ),
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('model_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dynamic.Model')),
            ],
            options={
            },
            bases=('dynamic.model',),
        ),
    ]
