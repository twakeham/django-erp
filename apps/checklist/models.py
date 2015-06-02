from django.db import models as db
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User

from core.dynamic.models import *
from core.form.models import ModelForm


class ChecklistFollowup(db.Model):
    user = db.ForeignKey(User)
    date = db.DateTimeField(auto_now_add=True)
    comment = db.TextField()
    photo = db.ImageField(upload_to='photo', blank=True)
    signature = db.ImageField(upload_to='media', blank=True)

    content_type = db.ForeignKey(ContentType)
    object_id = db.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Checklist(Model):
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Checklist, self).save(force_insert, force_update, using, update_fields)

        Relation.objects.get_or_create(model=self, name='followups', type=GENERIC, related_model=Model.objects.get(name='Checklistfollowup'))


