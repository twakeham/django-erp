from django.db import connection
from django.db.models import ManyToManyRel
from django.apps import apps
from django.forms.models import model_to_dict
from django.contrib.contenttypes.models import ContentType

from core.dynamic.models.fields import *

from fields import REVERSE_FIELD_MAP, REVERSE_RELATION_MAP, MANY_TO_MANY, Field, Relation


class Model(db.Model):
    '''
        Dynamodel database representation
    '''

    class Meta:
        verbose_name = 'Data store'
        verbose_name_plural = 'Data stores'

    def __unicode__(self):
        return self.name

    name = db.CharField(max_length=64, unique=True)
    verbose_name = db.CharField(max_length=64, blank=True, null=True, help_text='Human readable name for model')
    verbose_name_plural = db.CharField(max_length=64, blank=True, null=True, help_text='Plural form of verbose name.  Leave blank if standard pluralisation applies.')
    display_format = db.CharField(max_length=255, help_text='Formatting of record for display')
    description = db.TextField(blank=True, null=True)
    inherits = db.ForeignKey('self', related_name='children', blank=True, null=True, help_text='Inherit fields from another model')

    db_table = db.CharField(max_length=100, blank=True, verbose_name='Database table', help_text='Database table name, leave blank unless there is a reason')

    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)
        self._model = None

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains",)

    def _create_model(self, parent=None):
        '''
            Generates a Django model from a Model record.  Should only ever run once per model otherwise relationships
            fail to work correctly.
        '''

        model = self._create_deferred_relation_model(parent)
        self._contribute_relations(model)
        return model

    def _create_deferred_relation_model(self, parent=None):
        '''
            Generates a Django model from a Model record.  Creates a model without relations so as to avoid mutually
            recursive and self referential relationships from causing infinite recursion runtime errors.
        '''

        class Meta:
            app_label = 'udt'
            verbose_name = self.verbose_name or None
            verbose_name_plural = self.verbose_name_plural or None
            db_table = self.db_table

        def __unicode__(inst):
            return self.display_format.format(**model_to_dict(inst))


        fields = Field.objects.filter(basefield_ptr__model=self)

        attrs = {field.name: field._db_field() for field in fields}

        attrs['Meta'] = Meta
        attrs['__unicode__'] = __unicode__
        attrs['__module__'] = 'udt'
        attrs['deferred'] = True

        # this allows inheritance of models which are not defined by dynamic app but only at code level
        # mostly for auth app
        if parent is None:
            if self.inherits:
                inherited_model = self.inherits.model
                bases = (inherited_model, )
            else:
                bases = (db.Model, )
        else:
            bases = (parent, )

        return type(str(self.name), bases, attrs)

    def _contribute_relations(self, model):
        '''
            Contributes relationships to a deferred model so that django creates the appropriate database queries for
            data access.
        '''

        fields = Relation.objects.filter(basefield_ptr__model=self)

        for field in fields:
            db_field = field._db_field()
            db_field.contribute_to_class(model, field.name)

        model.deferred = False

        return model


    @property
    def model(self):
        '''
           Returns cached model or generates the model and returns it
        '''

        # special handling for model wrappers
        try:
            return self.modelwrapper.model
        except Model.DoesNotExist:
            try:
                return apps.get_model('udt', self.name)
            except:
                return self._create_model()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            # if the model hasn't got an id it's new and needs to have its database model created
            self._db_create_model()
            ContentType.objects.get_or_create(app_label='udt', model=self.name.lower(), name=self.verbose_name)

        if not self.db_table:
            # auto populate table name if it isn't supplied
            self.db_table = self.model._meta.db_table

        super(Model, self).save(force_insert, force_update, using, update_fields)

    @property
    def table_exists(self):
        '''
            Returns whether the current Model record has had its table created
        '''

        return self.model._meta.db_table in connection.introspection.table_names()

    def _db_create_model(self):
        '''
            Create database table
        '''
        if self.table_exists:
            return

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(self.model)

    def _db_delete_model(self):
        '''
            Remove database table
        '''
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(self.model)

    def delete(self, using=None):
        '''
            Deletes Model instance, removing all fields and deleting its database table
        '''
        fields = Field.objects.filter(basefield_ptr__model=self)
        for field in fields:
            field.delete()
        if self.table_exists:
            self._db_delete_model()
        super(Model, self).delete(using)

    def add_field(self, field):
        '''
            Creates a database column for the given Field instance
        '''
        db_field = self._model_add_field(field)
        self._db_add_field(db_field)

    def _model_add_field(self, field):
        '''
            Contributes Field to Django model class
        '''
        db_field = field._db_field()
        db_field.contribute_to_class(self.model, field.name)
        return db_field

    def _db_add_field(self, field):
        '''
            Creates database column for given Django field
        '''
        with connection.schema_editor() as schema_editor:
            schema_editor.add_field(self.model, field)

    def remove_field(self, field):
        '''
            Removes given Field instance from model and removes the appropriate table column
        '''
        db_field = self.model._meta.get_field_by_name(field.name)[0]
        self._db_remove_field(db_field)
        self._model_remove_field(field)

    def _model_remove_field(self, field):
        '''
            Removes given Field instance field from model.
        '''

        # removing fields requires cleaning up the relevant field caches so that django doesn't create queries that
        # include removed field names.

        meta = self.model._meta
        db_field = meta.get_field_by_name(field.name)[0]

        # Django automatically removes the 'through' table for many-to-many relationships
        if db_field.rel and isinstance(db_field.rel, ManyToManyRel):
            meta.local_many_to_many.remove(db_field)
            if hasattr(meta, '_m2m_cache'):
                del meta._m2m_cache

        else:
            meta.local_fields.remove(db_field)
            if hasattr(meta, '_field_cache'):
                del meta._field_cache
                del meta._field_name_cache
                try:
                    del meta.fields
                except AttributeError:
                    pass
                try:
                    del meta.concrete_fields
                except AttributeError:
                    pass
                try:
                    del meta.local_concrete_fields
                except AttributeError:
                    pass

        if hasattr(meta, '_name_map'):
            del meta._name_map

    def _db_remove_field(self, field):
        '''
            Removes given Django field column from table
        '''
        with connection.schema_editor() as schema_editor:
            schema_editor.remove_field(self.model, field)

    def alter_field(self, old, new):
        '''
            Attempts to alter database column to new Field instance.
        '''

        # this is fraught for things like type changes and needs some error checking around it to ensure that the user
        # receives a nice error message.  Possibility limit fields that the user can select for the current type -
        # eg, int -> char and float, date -> no changes allowed

        with connection.schema_editor() as schema_editor:
            new.column = old.column
            schema_editor.alter_field(self.model, old, new)


class ModelWrapper(Model):
    '''
        Creates a dynamodel, based on a hardcoded model, with virtual fields and relationships so that they can be
        the target of relations.
    '''

    class Meta:
        verbose_name = 'Data wrapper'
        verbose_name_plural = 'Data wrappers'

    def __unicode__(self):
        return self.name

    content_type = db.ForeignKey(ContentType, limit_choices_to=~db.Q(app_label='dynamic'))

    @property
    def model(self):
        '''
           Returns cached model or generates the model and returns it
        '''
        return self.content_type.model_class()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.name = self.model._meta.model_name.title()
            self.verbose_name = self.model._meta.verbose_name
            self.verbose_name_plural = self.model._meta.verbose_name_plural
            self.db_table = self.model._meta.db_table

            db.Model.save(self, force_insert, force_update, using, update_fields)

            # create virtual fields for the hard coded model (this is for apps that look at fields)
            for field in self.model._meta.fields:
                try:
                    # create normal data field
                    #print field.__class__
                    field_type = REVERSE_FIELD_MAP[field.__class__]
                    Field.objects.create(model=self, name=field.name, type=field_type, virtual=True)
                except KeyError:
                    try:
                        # create relation field
                        field_type = REVERSE_RELATION_MAP[field]
                        related_model = field.related.parent_model
                        related_name = related_model.model_name.title()
                        try:
                            # try getting dynamic model or wrapper
                            related_dynamic_model = Model.objects.get(name=related_name)
                        except Model.DoesNotExist:
                            # if it doesn't exist create it (for example creating a wrapper for auth.User will also
                            # create auth.Group and auth.Permission
                            related_dynamic_model = ModelWrapper.objects.create(content_type=ContentType.objects.get_for_model(related_model))
                        Relation.objects.create(model=self, name=related_name.lower(), type=field_type, related_model=related_dynamic_model, virtual=True)
                    except KeyError:
                        continue

            # create virtual m2m relations (they are handled separately in django)
            for field in self.model._meta.many_to_many:
                related_model = field.related.parent_model
                related_name = related_model._meta.model_name.title()
                try:
                    related_dynamic_model = Model.objects.get(name=related_name)
                except Model.DoesNotExist:
                    related_dynamic_model = ModelWrapper.objects.create(content_type=ContentType.objects.get_for_model(related_model))
                Relation.objects.create(model=self, name=related_name.lower(), type=MANY_TO_MANY, related_model=related_dynamic_model, virtual=True)

