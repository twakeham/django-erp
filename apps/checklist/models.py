from django.db import models as db

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from core.dynamic.models import *
from core.form.models import *
#from template.models import *


class Checklist(db.Model):

    form = db.ForeignKey(ModelForm, blank=True, null=True, related_name='preforms', verbose_name='Form', help_text='Form to be filled out prior to completing checklist.')
    followup_form = db.ForeignKey(ModelForm, blank=True, null=True, related_name='followup_forms', verbose_name='Followup form', help_text='Form to be used for followup.')

    require_id = db.BooleanField(default=True, help_text='Require user to login prior to completing checklist.')
    datestamp = db.BooleanField(default=True, help_text='Date stamp all entries.')



