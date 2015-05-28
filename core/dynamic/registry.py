from models.fields import *
from signals import fields_registered


# register standard data types
field_registry.register('Short Text', CharField, CHAR)
field_registry.register('Text', TextField, TEXT)
field_registry.register('Slug', SlugField, SLUG)
field_registry.register('Email', EmailField, EMAIL)
field_registry.register('URL', UrlField, URL)
field_registry.register('Boolean', BooleanField, BOOLEAN)
field_registry.register('Integer', IntegerField, INT)
field_registry.register('Big Integer', BigIntegerField, BIG_INT)
field_registry.register('Float', FloatField, FLOAT)
field_registry.register('Decimal', DecimalField, DECIMAL)
field_registry.register('Date', DateField, DATE)
field_registry.register('Time', TimeField, TIME)
field_registry.register('Date/Time', DateTimeField, DATETIME)
field_registry.register('File', FileField, FILE)
field_registry.register('Image', ImageField, IMAGE)

# emit signal so that plugins can register their own data types
fields_registered.send(sender=field_registry)