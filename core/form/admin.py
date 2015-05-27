from django.contrib import admin
from django.db.models import Q
from grappelli_nested.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from models import *


class ModelFormFieldInline(NestedTabularInline):
    model = ModelFormField
    extra = 1

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'field' and self.instance:
            # need to allow user to add inherited fields to form
            if self.instance.inherits:
                kwargs['queryset'] = BaseField.objects.filter(Q(model=self.instance) | Q(model=self.instance.inherits))
            else:
                kwargs['queryset'] = BaseField.objects.filter(model=self.instance)
        return super(ModelFormFieldInline, self).formfield_for_foreignkey(db_field, request=request, **kwargs)


class ModelFormFieldGroupInline(NestedStackedInline):
    model = ModelFormFieldGroup
    inlines = (ModelFormFieldInline, )
    extra = 0

    def get_inline_instances(self, request, obj=None):

        field_inline = ModelFormFieldInline(self.model, self.admin_site)
        field_inline.instance = self.instance

        return (field_inline, )


class ModelFormAdmin(NestedModelAdmin):
    raw_id_fields = ('model', )
    autocomplete_lookup_fields = {
        'fk': ('model', )
    }

    def change_view(self, request, obj_id, form_url='', extra_context=None):
        self.inlines = (ModelFormFieldGroupInline, )
        return super(ModelFormAdmin, self).change_view(request, obj_id)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []

        group_inline = ModelFormFieldGroupInline(self.model, self.admin_site)
        group_inline.instance = obj.model

        return (group_inline, )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('model', )
        return ()

admin.site.register(ModelForm, ModelFormAdmin)


