from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from core.dynamic.models import ModelWrapper


ModelWrapper.objects.get_or_create(content_type=ContentType.objects.get_for_model(User))

