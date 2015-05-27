from models.fields import *
from signals import fields_registered


# register standard data types
registry.register('Short Text', CharField, CHAR)
registry.register('Text', TextField, TEXT)
registry.register('Slug', SlugField, SLUG)
registry.register('Email', EmailField, EMAIL)
registry.register('URL', UrlField, URL)
registry.register('Boolean', BooleanField, BOOLEAN)
registry.register('Integer', IntegerField, INT)
registry.register('Big Integer', BigIntegerField, BIG_INT)
registry.register('Float', FloatField, FLOAT)
registry.register('Decimal', DecimalField, DECIMAL)
registry.register('Date', DateField, DATE)
registry.register('Time', TimeField, TIME)
registry.register('Date/Time', DateTimeField, DATETIME)
registry.register('File', FileField, FILE)
registry.register('Image', ImageField, IMAGE)

# emit signal so that plugins can register their own data types
fields_registered.send(sender=registry)