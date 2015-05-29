from django.db import models as db

from core.dynamic.models import Model
from core.dynamic.models.fields import BaseField

from forms import FieldsetModelForm


class ModelForm(db.Model):
    """
        Database representation of forms for manipulation of dynamodels
    """

    class Meta:
        verbose_name = 'Model form'

    def __unicode__(self):
        return self.name

    name = db.CharField(max_length=64)
    description = db.TextField(blank=True)

    model = db.ForeignKey(Model)

    @property
    def form(self):
        groups = []
        for group in self.groups.all().order_by('sort_order'):
            fields = []
            for field in group.fields.all().order_by('sort_order'):
                fields.append(field.field.name)
            groups.append(
                (group.caption, {
                    'fields': fields,
                    'description': group.description
                })
            )

        class Meta:
            model = self.model.model
            fieldsets = groups

        return type(str(self.name), (FieldsetModelForm, ), {'Meta': Meta})


class ModelFormFieldGroup(db.Model):
    """
        Database representation of form fieldsets for manipulation of dynamodels
    """

    class Meta:
        verbose_name = 'Form field group'
        unique_together = ('caption', 'form')


    def __unicode__(self):
        return self.caption

    form = db.ForeignKey('ModelForm', related_name='groups')

    caption = db.CharField(max_length=64, blank=True, help_text='Leave blank for ungrouped fields')
    description = db.TextField(blank=True)
    sort_order = db.PositiveIntegerField(default=0)


class ModelFormField(db.Model):

    class Meta:
        verbose_name = 'Form field'
        ordering = ('sort_order', )

    def __unicode__(self):
        return self.field.name

    group = db.ForeignKey('ModelFormFieldGroup', related_name='fields')
    field = db.ForeignKey(BaseField)
    widget_override = db.CharField(max_length=32, blank=True)
    sort_order = db.PositiveIntegerField(default=0)


