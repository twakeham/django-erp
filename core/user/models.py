from django.db import models as db
from django.contrib.auth.models import User

from core.dynamic.models.fields import ExtendedFieldOption, Field
from core.user.fields import UserField


class AutoUserField(ExtendedFieldOption):
    """
        Database model for automatically filling a user
    """

    class Meta:
        verbose_name = 'Authenticated user field'

    field = db.OneToOneField(Field, related_name='autouserfield')

    def _db_field(self, attrs):
        return UserField(User, null=attrs['null'], blank=attrs['blank'])