# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('verbose_name', models.CharField(max_length=64, blank=True)),
                ('help_text', models.CharField(max_length=255, null=True, blank=True)),
                ('required', models.BooleanField(default=False)),
                ('unique', models.BooleanField(default=False)),
                ('sort_order', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BigIntegerField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default', models.BigIntegerField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Big integer field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BooleanField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Boolean field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CharField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_length', models.IntegerField(default=50)),
                ('choices', models.TextField(help_text=b'Enter one choice per line', blank=True)),
                ('default', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'Character field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DateField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auto_now', models.BooleanField(default=False, help_text=b'Set this field to current date when record is saved')),
                ('auto_now_add', models.BooleanField(default=False, help_text=b'Set this field to current date when record is created')),
                ('default', models.DateField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Date field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DateTimeField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auto_now', models.BooleanField(default=False, help_text=b'Set this field to current date/time when record is saved')),
                ('auto_now_add', models.BooleanField(default=False, help_text=b'Set this field to current date/time when record is created')),
                ('default', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Date/time field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DecimalField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_digits', models.IntegerField()),
                ('decimal_places', models.IntegerField()),
                ('default', models.DecimalField(max_digits=20, decimal_places=20)),
            ],
            options={
                'verbose_name': 'Decimal field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_length', models.IntegerField(default=75)),
                ('default', models.EmailField(max_length=75, blank=True)),
            ],
            options={
                'verbose_name': 'Email field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('basefield_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dynamic.BaseField')),
                ('type', models.IntegerField()),
                ('primary_key', models.BooleanField(default=False, verbose_name=b'PK')),
                ('index', models.BooleanField(default=False)),
                ('virtual', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Field',
            },
            bases=('dynamic.basefield',),
        ),
        migrations.CreateModel(
            name='FieldRegistryData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('module', models.CharField(max_length=128)),
                ('classname', models.CharField(max_length=64)),
                ('accessor', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FileField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_length', models.IntegerField(default=100)),
                ('field', models.OneToOneField(related_name='filefield', to='dynamic.Field')),
            ],
            options={
                'verbose_name': 'File field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FloatField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default', models.FloatField(null=True, blank=True)),
                ('field', models.OneToOneField(related_name='floatfield', to='dynamic.Field')),
            ],
            options={
                'verbose_name': 'Float field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImageField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_length', models.IntegerField(default=100)),
                ('field', models.OneToOneField(related_name='imagefield', to='dynamic.Field')),
            ],
            options={
                'verbose_name': 'Image field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IntegerField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default', models.IntegerField(null=True, blank=True)),
                ('field', models.OneToOneField(related_name='integerfield', to='dynamic.Field')),
            ],
            options={
                'verbose_name': 'Integer field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('verbose_name', models.CharField(help_text=b'Human readable name for model', max_length=64, null=True, blank=True)),
                ('verbose_name_plural', models.CharField(help_text=b'Plural form of verbose name.  Leave blank if standard pluralisation applies.', max_length=64, null=True, blank=True)),
                ('display_format', models.CharField(help_text=b'Formatting of record for display', max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('db_table', models.CharField(help_text=b'Database table name, leave blank unless there is a reason', max_length=100, verbose_name=b'Database table', blank=True)),
            ],
            options={
                'verbose_name': 'Data store',
                'verbose_name_plural': 'Data stores',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModelWrapper',
            fields=[
                ('model_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dynamic.Model')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Data wrapper',
                'verbose_name_plural': 'Data wrappers',
            },
            bases=('dynamic.model',),
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('basefield_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='dynamic.BaseField')),
                ('type', models.IntegerField(choices=[(30, b'Foreign Key'), (31, b'Many to Many'), (32, b'One to One')])),
                ('reverse_name', models.CharField(max_length=64, blank=True)),
                ('virtual', models.BooleanField(default=False)),
                ('related_model', models.ForeignKey(related_name='reverse', to='dynamic.Model')),
            ],
            options={
                'verbose_name': 'Relation',
            },
            bases=('dynamic.basefield',),
        ),
        migrations.CreateModel(
            name='SlugField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_length', models.IntegerField(default=50)),
                ('default', models.CharField(max_length=255, blank=True)),
                ('field', models.OneToOneField(related_name='slugfield', to='dynamic.Field')),
                ('populate_from', models.ForeignKey(related_name='slugs', blank=True, to='dynamic.CharField', null=True)),
            ],
            options={
                'verbose_name': 'Slug field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TextField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_length', models.IntegerField(null=True, blank=True)),
                ('default', models.TextField(blank=True)),
                ('field', models.OneToOneField(related_name='textfield', to='dynamic.Field')),
            ],
            options={
                'verbose_name': 'Text field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default', models.TimeField(null=True, blank=True)),
                ('field', models.OneToOneField(related_name='timefield', to='dynamic.Field')),
            ],
            options={
                'verbose_name': 'Time field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UploadLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Upload location',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UrlField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_length', models.IntegerField(default=200)),
                ('default', models.URLField(blank=True)),
                ('field', models.OneToOneField(related_name='urlfield', to='dynamic.Field')),
            ],
            options={
                'verbose_name': 'URL field',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='model',
            name='inherits',
            field=models.ForeignKey(related_name='children', blank=True, to='dynamic.Model', help_text=b'Inherit fields from another model', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagefield',
            name='upload_to',
            field=models.ForeignKey(related_name='images', to='dynamic.UploadLocation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='filefield',
            name='upload_to',
            field=models.ForeignKey(related_name='files', to='dynamic.UploadLocation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailfield',
            name='field',
            field=models.OneToOneField(related_name='emailfield', to='dynamic.Field'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='decimalfield',
            name='field',
            field=models.OneToOneField(related_name='decimalfield', to='dynamic.Field'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datetimefield',
            name='field',
            field=models.OneToOneField(related_name='datetimefield', to='dynamic.Field'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datefield',
            name='field',
            field=models.OneToOneField(related_name='datefield', to='dynamic.Field'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='charfield',
            name='field',
            field=models.OneToOneField(related_name='charfield', to='dynamic.Field'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booleanfield',
            name='field',
            field=models.OneToOneField(related_name='booleanfield', to='dynamic.Field'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bigintegerfield',
            name='field',
            field=models.OneToOneField(related_name='bigintegerfield', to='dynamic.Field'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='basefield',
            name='model',
            field=models.ForeignKey(to='dynamic.Model'),
            preserve_default=True,
        ),
    ]
