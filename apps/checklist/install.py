from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType

from core.dynamic.models import ModelWrapper

from models import *

if 'core.user' not in settings.INSTALLED_APPS:
    raise ImproperlyConfigured('core.users must be installed to use checklist app')

if 'core.template' not in settings.INSTALLED_APPS:
    raise ImproperlyConfigured('core.template must be installed to use checklist app')


ModelWrapper.objects.get_or_create(content_type=ContentType.objects.get_for_model(ChecklistFollowup))






