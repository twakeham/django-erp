from django.db import models as db


BIG_INT = 2
BOOLEAN = 4
CHAR = 5
DATE = 6
DATETIME = 7
DECIMAL = 8
EMAIL = 9
FILE = 10
FILEPATH = 11
FLOAT = 12
IMAGE = 13
INT = 14
IP_ADDR = 15
SLUG = 16
TEXT = 18
TIME = 19
URL = 20
USER = 21

FOREIGN_KEY = 30
MANY_TO_MANY = 31
ONE_TO_ONE = 32

RELATION_CHOICES = (
    (FOREIGN_KEY, 'Foreign Key'),
    (MANY_TO_MANY, 'Many to Many'),
    (ONE_TO_ONE, 'One to One')
)

FIELD_CHOICES = (
    (CHAR, 'Short Text'),
    (TEXT, 'Text'),
    (SLUG, 'Slug'),
    (EMAIL, 'Email'),
    (URL, 'URL'),
    (BOOLEAN, 'Boolean'),
    (INT, 'Integer'),
    (BIG_INT, 'Big Integer'),
    (FLOAT, 'Floating Point Number'),
    (DECIMAL, 'Decimal'),
    (DATE, 'Date'),
    (TIME, 'Time'),
    (DATETIME, 'Date/Time'),
    (FILE, 'File'),
    (IMAGE, 'Image'),
    (USER, 'User')
)

FIELD_MAP = {
    CHAR: 'charfield',
    TEXT: 'textfield',
    SLUG: 'slugfield',
    EMAIL: 'emailfield',
    URL: 'urlfield',
    BOOLEAN: 'booleanfield',
    INT: 'integerfield',
    BIG_INT: 'bigintegerfield',
    FLOAT: 'floatfield',
    DECIMAL: 'decimalfield',
    DATE: 'datefield',
    TIME: 'timefield',
    DATETIME: 'datetimefield',
    FILEPATH: 'filepathfield',
    FILE: 'filefield',
    IMAGE: 'imagefield',
    USER: 'userfield',
    IP_ADDR: 'ipaddress',
    FOREIGN_KEY: 'foreignkey'
}


class FieldRegistryData(db.Model):
    '''
        Create unique ids for fields so that we always get the same field for a given id
    '''
    name = db.CharField(max_length=64)


class FieldRegistry(object):

    _registry = {}

    def __init__(self):
        super(FieldRegistry, self).__init__()
        self._field_map = {}
        self._field_choices = []
        self._db_field_map = {}

    def __iter__(self):
        return iter(self.field_choices)

    @property
    def field_choices(self):
        if not self._field_choices:
            self._generate_field_choices()
        return self._field_choices

    def _generate_field_choices(self):
        self._field_choices = []
        for field_name, (extended_opts, id) in FieldRegistry._registry.iteritems():
            self._field_choices.append((id, field_name))

    @property
    def db_field_map(self):
        if not self._db_field_map:
            self._generate_db_field_map()
        return self._db_field_map

    def _generate_db_field_map(self):
        self._db_field_map = {}


    @property
    def field_map(self):
        if not self._field_map:
            self._generate_field_map()
        return self._field_map

    def _generate_field_map(self):
        self._field_map = {}
        for field_name, (extended_opts, id) in FieldRegistry._registry.iteritems():
            field = extended_opts._meta.get_field_by_name('field')
            related_name = field.rel.related_name
            self._field_map[id] = related_name

    def register(self, name, extended_opts):
        data_obj = FieldRegistryData.objects.get_or_create(name=name)
        FieldRegistry._registry[name] = (extended_opts, data_obj.id)

        self._generate_field_map()
        self._generate_field_choices()



class UploadLocation(db.Model):
    """
        Database model to represent locations that file and image fields can upload to
    """

    class Meta:
        verbose_name = 'Upload location'

    def __unicode__(self):
        return self.path

    path = db.CharField(max_length=255)


class BaseField(db.Model):
    """
        Abstract database model to represent dynamodel fields and relationships
    """

    # class Meta:
    #     abstract = True

    def __unicode__(self):
        return self.name

    model = db.ForeignKey('Model')

    name = db.CharField(max_length=64)
    verbose_name = db.CharField(max_length=64, blank=True)
    help_text = db.CharField(max_length=255, blank=True, null=True)
    required = db.BooleanField(default=False)
    unique = db.BooleanField(default=False)

    sort_order = db.IntegerField(blank=True, null=True)

    def _data_equality(self, other):
        '''
            Compare data between this record and another
            (Django model equality only checks that the class is the same)
        '''
        if self.__class__ is not other.__class__:
            raise ValueError('Both classes must be the same')

        for field in self._meta.fields:
            if getattr(self, field.name, None) != getattr(other, field.name, None):
                return False

        return True

    @property
    def specific(self):
        try:
            return self.field
        except AttributeError:
            return self.relation


class Field(BaseField):
    """
        Database model to represent dynamodel fields
    """

    class Meta:
        verbose_name = 'Field'
        #unique_together = ['model', 'name']


    type = db.IntegerField(choices=FIELD_CHOICES)
    primary_key = db.BooleanField(default=False, verbose_name='PK')
    index = db.BooleanField(default=False)

    virtual = db.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
            Saves the current instance.
        """

        # virtual fields (for wrappers around hard coded models) don't do db management
        if self.virtual:
            super(Field, self).save(force_insert, force_update, using, update_fields)
            return

        exists = self.id

        if exists:
            existing = Field.objects.get(pk=self.id)
            if not self._data_equality(existing):

                super(Field, self).save(force_insert, force_update, using, update_fields)

                # if the field type has changed we need to delete the old subfield data and create
                # the appropriate new subtype
                if existing.type != self.type:
                    existing.specific.delete()

                    # create subfield data settings
                    field_type = DB_FIELD_MAP[self.type]
                    field = field_type(field=self)
                    field.save()

                existing_field = self.model.model._meta.get_field_by_name(existing.name)[0]
                new_field = self._db_field()

                # make the required changes to the database
                self.model._model_remove_field(existing)
                self.model._model_add_field(self)

                self.model.alter_field(existing_field, new_field)

        else:
            super(Field, self).save(force_insert, force_update, using, update_fields)

            # create subfield data settings
            field_type = DB_FIELD_MAP[self.type]
            field = field_type(field=self)
            field.save()

            self.model.add_field(self)

        if not self.sort_order:
            self.sort_order = self.id
            self.save()

    def delete(self, using=None):
        '''
            Deletes the current instance
        '''
        self.model.remove_field(self)

        field_attr = FIELD_MAP[self.type]
        specific = getattr(self, field_attr, None)
        specific.delete()

        super(Field, self).delete(using)

    @property
    def specific(self):
        '''
            Return the subfield for this field
        '''
        field_attr = FIELD_MAP[self.type]
        return getattr(self, field_attr, None)

    def _db_field(self):
        """
            Internal function to generate generic field attributes
        """
        return self.specific._db_field({
            'verbose_name': self.verbose_name,
            'help_text': self.help_text,
            'blank': not self.required,
            'null': not self.required,
            'unique': self.unique,
            'primary_key': self.primary_key,
            'db_index': self.index or None,
        })


class Relation(BaseField):
    """
        Database model to represent dynamodel relations
    """

    class Meta:
        verbose_name = 'Relation'
        #nique_together = ['model', 'name']

    type = db.IntegerField(choices=RELATION_CHOICES)
    related_model = db.ForeignKey('Model', related_name='reverse')
    reverse_name = db.CharField(max_length=64, blank=True)

    virtual = db.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
            Saves the current instance.
        """

        # handle wrappers around hard coded models separately
        if self.virtual:
            super(Relation, self).save(force_insert, force_update, using, update_fields)
            return

        if not self.reverse_name:
            self.reverse_name = '{0}_{1}'.format(self.model.name, self.name)

        exists = self.id

        if exists:
            existing = Relation.objects.get(pk=self.pk)
            if not self._data_equality(existing):

                super(Relation, self).save(force_insert, force_update, using, update_fields)

                existing_field = self.model.model._meta.get_field_by_name(existing.name)[0]
                new_field = self._db_field()

                self.model._model_remove_field(existing)
                self.model._model_add_field(self)

                self.model.alter_field(existing_field, new_field)

        else:
            super(Relation, self).save(force_insert, force_update, using, update_fields)

            self.model.add_field(self)

    def delete(self, using=None):
        '''
            Deletes the current instance
        '''
        self.model.remove_field(self)

    def _db_field(self):
        """
            Internal function to generate generic relation attributes
        """
        type = RELATED_FIELD_MAP[self.type]
        attrs = {
            'verbose_name': self.verbose_name,
            'help_text': self.help_text,
            'blank': not self.required,
            'null': not self.required,
            'unique': self.unique,
            'related_name': self.reverse_name
        }

        # special handling for self referential relationships
        if self.related_model.name == self.name:
            return type('self', **attrs)
        else:
            try:
                # try to create relation field
                return type(self.related_model.name, **attrs)
            except ValueError:
                # if related model has not been evaluated by django yet, we need to expose it, but need to be careful
                # of mutually recursive relationships between models creating runtime exceptions, so create a model
                # sans relations, create the relationship then contribute the other models relations
                model = self.related_model._create_deferred_relation_model()
                relation_field = type(self.related_model.name, **attrs)
                self.related_model._contribute_relations(model)
                return relation_field


#class RelationWrapper(Relation):



class ExtendedFieldOption(db.Model):
    '''
        Base subfield options and save mechanics.  Abstract model.
    '''

    class Meta:
        abstract = True

    def __unicode__(self):
        return '{0} : {1}'.format(self.field.model.name, self.field.name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            return super(ExtendedFieldOption, self).save(force_insert, force_update, using, update_fields)

        model = self.field.model.model
        existing = Field.objects.get(pk=self.field.pk)
        existing_field = model._meta.get_field_by_name(existing.name)[0]

        super(ExtendedFieldOption, self).save(force_insert, force_update, using, update_fields)

        self.field.model._model_remove_field(existing)
        self.field.model._model_add_field(self.field)

        new_field = self.field._db_field()

        self.field.model.alter_field(existing_field, new_field)


class CharField(ExtendedFieldOption):
    """
        Database model for character fields on dynamodels
    """

    class Meta:
        verbose_name = 'Character field'

    field = db.OneToOneField('Field', related_name='charfield')

    max_length = db.IntegerField(default=50)
    choices = db.TextField(blank=True, help_text='Enter one choice per line')
    default = db.CharField(max_length=255, blank=True)

    def _db_field(self, attrs):
        if self.choices:
            choices = self.choices.replace('\r', '').split('\n')
            choices = zip(choices, choices)
            attrs ['choices'] = choices

        attrs.update({
            'max_length': self.max_length,
            'default': self.default or None
        })
        return db.CharField(**attrs)


class TextField(ExtendedFieldOption):
    """
        Database model for text fields on dynamodels
    """

    class Meta:
        verbose_name = 'Text field'

    field = db.OneToOneField('Field', related_name='textfield')

    max_length = db.IntegerField(blank=True, null=True)
    default = db.TextField(blank=True)

    def _db_field(self, attrs):
        attrs.update({
            'max_length': self.max_length or None,
            'default': self.default or None
        })
        return db.TextField(**attrs)


class SlugField(ExtendedFieldOption):
    """
        Database model for slugfields fields on dynamodels
    """

    class Meta:
        verbose_name = 'Slug field'

    field = db.OneToOneField('Field', related_name='slugfield')

    max_length = db.IntegerField(default=50)
    default = db.CharField(max_length=255, blank=True)
    populate_from = db.ForeignKey('CharField', blank=True, null=True, related_name='slugs')

    def _db_field(self, attrs):
        attrs.update({
            'max_length': self.max_length or None,
            'default': self.default or None
        })
        return db.SlugField(**attrs)


class EmailField(ExtendedFieldOption):
    """
        Database model for emailfields fields on dynamodels
    """

    class Meta:
        verbose_name = 'Email field'

    field = db.OneToOneField('Field', related_name='emailfield')

    max_length = db.IntegerField(default=75)
    default = db.EmailField(blank=True)

    def _db_field(self, attrs):
        attrs.update({
            'max_length': self.max_length or None,
            'default': self.default or None
        })
        return db.EmailField(**attrs)


class UrlField(ExtendedFieldOption):
    """
        Database model for urlfields fields on dynamodels
    """

    class Meta:
        verbose_name = 'URL field'

    field = db.OneToOneField('Field', related_name='urlfield')

    max_length = db.IntegerField(default=200)
    default = db.URLField(blank=True)

    def _db_field(self, attrs):
        attrs.update({
            'max_length': self.max_length or None,
            'default': self.default or None
        })
        return db.URLField(**attrs)


class BooleanField(ExtendedFieldOption):
    """
        Database model for boolfields fields on dynamodels
    """

    class Meta:
        verbose_name = 'Boolean field'

    field = db.OneToOneField('Field', related_name='booleanfield')

    default = db.BooleanField(default=False)

    def _db_field(self, attrs): 
        attrs.update({
            'default': self.default or None
        })
        return db.BooleanField(**attrs)


class IntegerField(ExtendedFieldOption):
    """
        Database model for integerfields fields on dynamodels
    """

    class Meta:
        verbose_name = 'Integer field'

    field = db.OneToOneField('Field', related_name='integerfield')

    default = db.IntegerField(blank=True, null=True)

    def _db_field(self, attrs):
        attrs.update({
            'default': self.default or None
        })
        return db.IntegerField(**attrs)


class BigIntegerField(ExtendedFieldOption):
    """
        Database model for bigintegerfields fields on dynamodels
    """

    class Meta:
        verbose_name = 'Big integer field'

    field = db.OneToOneField('Field', related_name='bigintegerfield')

    default = db.BigIntegerField(blank=True, null=True)

    def _db_field(self, attrs):
        attrs.update({
            'default': self.default or None
        })
        return db.BigIntegerField(**attrs)


class FloatField(ExtendedFieldOption):
    """
        Database model for float fields on dynamodels
    """

    class Meta:
        verbose_name = 'Float field'

    field = db.OneToOneField('Field', related_name='floatfield')

    default = db.FloatField(blank=True, null=True)

    def _db_field(self, attrs):
        attrs.update({
            'default': self.default or None
        })
        return db.FloatField(**attrs)


class DecimalField(ExtendedFieldOption):
    """
        Database model for decimalfields on dynamodels
    """

    class Meta:
        verbose_name = 'Decimal field'

    field = db.OneToOneField('Field', related_name='decimalfield')

    max_digits = db.IntegerField()
    decimal_places = db.IntegerField()
    default = db.DecimalField(max_digits=20, decimal_places=20)

    def _db_field(self, attrs):
        attrs.update({
            'max_digits': self.max_digits,
            'decimal_places': self.decimal_places,
            'default': self.default or None
        })
        return db.DecimalField(**attrs)


class DateField(ExtendedFieldOption):
    """
        Database model for datefields on dynamodels
    """

    class Meta:
        verbose_name = 'Date field'

    field = db.OneToOneField('Field', related_name='datefield')

    auto_now = db.BooleanField(default=False, help_text='Set this field to current date when record is saved')
    auto_now_add = db.BooleanField(default=False, help_text='Set this field to current date when record is created')
    default = db.DateField(blank=True, null=True)

    def _db_field(self, attrs):
        attrs.update({
            'auto_now': self.auto_now or False,
            'auto_now_add': self.auto_now_add or False,
            'default': self.default or None
        })
        return db.DateField(**attrs)


class TimeField(ExtendedFieldOption):
    """
        Database model for timefields on dynamodels
    """

    class Meta:
        verbose_name = 'Time field'

    field = db.OneToOneField('Field', related_name='timefield')

    default = db.TimeField(blank=True, null=True)

    def _db_field(self, attrs):
        attrs.update({
            'default': self.default or None
        })
        return db.TimeField(**attrs)


class DateTimeField(ExtendedFieldOption):
    """
        Database model for datetimefields on dynamodels
    """

    class Meta:
        verbose_name = 'Date/time field'

    field = db.OneToOneField('Field', related_name='datetimefield')

    auto_now = db.BooleanField(default=False, help_text='Set this field to current date/time when record is saved')
    auto_now_add = db.BooleanField(default=False, help_text='Set this field to current date/time when record is created')
    default = db.DateTimeField(blank=True, null=True)

    def _db_field(self, attrs):
        attrs.update({
            'auto_now': self.auto_now or False,
            'auto_now_add': self.auto_now_add or False,
            'default': self.default or None
        })
        return db.DateTimeField(**attrs)


class FileField(ExtendedFieldOption):
    """
        Database model for filefields on dynamodels
    """

    class Meta:
        verbose_name = 'File field'

    field = db.OneToOneField('Field', related_name='filefield')

    upload_to = db.ForeignKey('UploadLocation', related_name='files')
    max_length = db.IntegerField(default=100)

    def _db_field(self, attrs):
        attrs.update({
            'upload_to': self.upload_to.path,
            'max_length': self.max_length
        })
        return db.FileField(**attrs)


class ImageField(ExtendedFieldOption):
    """
        Database model for imagefields on dynamodels
    """

    class Meta:
        verbose_name = 'Image field'

    field = db.OneToOneField('Field', related_name='imagefield')


    upload_to = db.ForeignKey('UploadLocation', related_name='images')
    max_length = db.IntegerField(default=100)

    def _db_field(self, attrs):
        attrs.update({
            'upload_to': self.upload_to.path,
            'max_length': self.max_length
        })
        return db.ImageField(**attrs)


DB_FIELD_MAP = {
    CHAR: CharField,
    TEXT: TextField,
    SLUG: SlugField,
    EMAIL: EmailField,
    URL: UrlField,
    BOOLEAN: BooleanField,
    INT: IntegerField,
    BIG_INT: BigIntegerField,
    FLOAT: FloatField,
    DECIMAL: DecimalField,
    DATE: DateField,
    TIME: TimeField,
    DATETIME: DateTimeField,
    FILE: FileField,
    IMAGE: ImageField,
}

REVERSE_FIELD_MAP = {
    db.CharField: CHAR,
    db.TextField: TEXT,
    db.SlugField: SLUG,
    db.EmailField: EMAIL,
    db.URLField: URL,
    db.BooleanField: BOOLEAN,
    db.IntegerField: INT,
    db.FloatField: FLOAT,
    db.BigIntegerField: BIG_INT,
    db.DecimalField: DECIMAL,
    db.DateField: DATE,
    db.TimeField: TIME,
    db.DateTimeField: DATETIME,
    db.FileField: FILE,
    db.ImageField: IMAGE
}

RELATED_FIELD_MAP = {
    FOREIGN_KEY: db.ForeignKey,
    MANY_TO_MANY: db.ManyToManyField,
    ONE_TO_ONE: db.OneToOneField
}


REVERSE_RELATION_MAP = dict(zip(RELATED_FIELD_MAP.values(), RELATED_FIELD_MAP.keys()))