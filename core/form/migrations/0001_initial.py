# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(blank=True)),
                ('model', models.ForeignKey(to='dynamic.Model')),
            ],
            options={
                'verbose_name': 'Model form',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModelFormField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('widget_override', models.CharField(max_length=32, blank=True)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('field', models.ForeignKey(to='dynamic.BaseField')),
            ],
            options={
                'ordering': ('sort_order',),
                'verbose_name': 'Form field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModelFormFieldGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.CharField(help_text=b'Leave blank for ungrouped fields', max_length=64, blank=True)),
                ('description', models.TextField(blank=True)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('form', models.ForeignKey(related_name='groups', to='form.ModelForm')),
            ],
            options={
                'verbose_name': 'Form field group',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='modelformfieldgroup',
            unique_together=set([('caption', 'form')]),
        ),
        migrations.AddField(
            model_name='modelformfield',
            name='group',
            field=models.ForeignKey(related_name='fields', to='form.ModelFormFieldGroup'),
            preserve_default=True,
        ),
    ]
