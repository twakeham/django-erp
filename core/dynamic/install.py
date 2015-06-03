from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType

from core.dynamic.models import ModelWrapper
from core.dynamic.models.fields import field_registry, UploadLocation


if 'django.contrib.contenttypes' not in settings.INSTALLED_APPS:
    raise ImproperlyConfigured('Content Types must be installed for LaunchPad ERP')

ModelWrapper.objects.get_or_create(content_type=ContentType.objects.get_for_model(ContentType))

UploadLocation.objects.get_or_create(id=1, path='files/')

# register standard data types
field_registry.register('Short Text', 'core.dynamic.models.fields.CharField')
field_registry.register('Text', 'core.dynamic.models.fields.TextField')
field_registry.register('Slug', 'core.dynamic.models.fields.SlugField')
field_registry.register('Email', 'core.dynamic.models.fields.EmailField')
field_registry.register('URL', 'core.dynamic.models.fields.UrlField')
field_registry.register('Boolean', 'core.dynamic.models.fields.BooleanField')
field_registry.register('Integer', 'core.dynamic.models.fields.IntegerField')
field_registry.register('Big Integer', 'core.dynamic.models.fields.BigIntegerField')
field_registry.register('Float', 'core.dynamic.models.fields.FloatField')
field_registry.register('Decimal', 'core.dynamic.models.fields.DecimalField')
field_registry.register('Date', 'core.dynamic.models.fields.DateField')
field_registry.register('Time', 'core.dynamic.models.fields.TimeField')
field_registry.register('Date/Time', 'core.dynamic.models.fields.DateTimeField')
field_registry.register('File', 'core.dynamic.models.fields.FileField')
field_registry.register('Image', 'core.dynamic.models.fields.ImageField')