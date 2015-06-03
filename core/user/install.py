from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from core.dynamic.models import ModelWrapper, field_registry

# ensure that django.contrib.auth models have wrappers or create them
ModelWrapper.objects.get_or_create(content_type=ContentType.objects.get_for_model(User))

# register new dynamic field type
field_registry.register('User', 'core.user.models.AutoUserField')