from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from core.dynamic.models import *

if 'core.user' not in settings.INSTALLED_APPS:
    raise ImproperlyConfigured('core.users must be installed to use userprofile app')


User = Model.objects.get(name='User')
UserProfile, created = Model.objects.get_or_create(name='UserProfile', display_format='{user.first_name} {user.last_name}')

if created:
    user = Relation(model=UserProfile, name='user', type=ONE_TO_ONE, related_model=User)
    user.reverse_name = 'profile'
    user.save()