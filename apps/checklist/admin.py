from django.contrib import admin


from django.contrib import admin
from django.core import urlresolvers

from apps.checklist.models import *


class DynamicFieldInline(admin.TabularInline):
    extra = 0
    model = Field
    readonly_fields = ('edit_link', )
    fields = ('name', 'type', 'verbose_name', 'help_text', 'required', 'unique', 'primary_key', 'index', 'edit_link')

    def edit_link(self, inst):
        '''
            Returns a link to the subfield admin edit page
        '''

        if not inst.pk:
            return None

        try:
            return '<a href="{0}?_popup=1" onclick="return showAddAnotherPopup(this);">Advanced settings</a>'.format(urlresolvers.reverse('fieldadmin:dynamic_{0}_change'.format(field_registry.field_map[inst.type]), args=(inst.specific.pk, )))
        except urlresolvers.NoReverseMatch:
            return None

    edit_link.verbose_name = 'Advanced settings'
    edit_link.allow_tags = True


class DynamicRelationInline(admin.TabularInline):
    extra = 0
    model = Relation
    fk_name = 'model'
    fields = ('name', 'type', 'related_model', 'reverse_name', 'verbose_name', 'help_text', 'required', 'unique')


class ChecklistAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['name', 'inherits']}),
        ('Display', {'fields': ['verbose_name', 'verbose_name_plural', 'display_format'], 'classes': ('collapse', )}),
    ]

    def get_readonly_fields(self, request, obj=None):
        '''
            Stops editing of inherits and db_table field after initial save as this doesn't make sense to allow
        '''
        if not obj:
            return []
        return ('inherits', 'db_table')

    def save_model(self, request, obj, form, change):
        super(ChecklistAdmin, self).save_model(request, obj, form, change)

    def get_inline_instances(self, request, obj=None):
        if obj:
            return DynamicFieldInline(self.model, self.admin_site), DynamicRelationInline(self.model, self.admin_site)
        return super(ChecklistAdmin, self).get_inline_instances(request, obj)


admin.site.register(Checklist, ChecklistAdmin)

