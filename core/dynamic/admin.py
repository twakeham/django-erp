from django.contrib import admin
from django.core import urlresolvers

from core.dynamic.models import *
from core.dynamic.models.fields import *


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


class FieldAdmin(admin.ModelAdmin):
    exclude = ('field', )

    list_display = ('model_name', 'field_name')
    list_display_links = ('field_name', )

    def model_name(self, inst):
        '''
            Returns a link to the model that this subfield belongs to for easy editing
        '''
        url = urlresolvers.reverse('admin:dynamic_model_change', args=(inst.field.model.pk, ))
        return '<a href="{0}">{1}</a>'.format(url, inst.field.model.name)
    model_name.allow_tags = True

    def field_name(self, inst):
        '''
            Returns the fields name
        '''
        return inst.field.name

# this is kind of a hack to hide the field admins from the main admin site but still allow users to edit
# field specific options
fieldadmin = admin.AdminSite('fieldadmin')
fieldadmin.register(CharField, FieldAdmin)
fieldadmin.register(TextField, FieldAdmin)
fieldadmin.register(SlugField, FieldAdmin)
fieldadmin.register(EmailField, FieldAdmin)
fieldadmin.register(BooleanField, FieldAdmin)
fieldadmin.register(IntegerField, FieldAdmin)
fieldadmin.register(BigIntegerField, FieldAdmin)
fieldadmin.register(FloatField, FieldAdmin)
fieldadmin.register(DecimalField, FieldAdmin)
fieldadmin.register(DateField, FieldAdmin)
fieldadmin.register(TimeField, FieldAdmin)
fieldadmin.register(DateTimeField, FieldAdmin)
fieldadmin.register(FileField, FieldAdmin)
fieldadmin.register(ImageField, FieldAdmin)


class DynamicModelAdmin(admin.ModelAdmin):

    inlines = (DynamicFieldInline, DynamicRelationInline)
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
        super(DynamicModelAdmin, self).save_model(request, obj, form, change)
        print

    #def get_queryset(self, request):
    #    qs = super(DynamicModelAdmin, self).get_queryset(request)
    #    return qs.filter(modelwrapper__isnull=True)

admin.site.register(Model, DynamicModelAdmin)


class ModelWrapperFieldInline(admin.TabularInline):
    extra = 0
    max_num = 0
    model = Field
    can_delete = False
    fields = ('name', 'type', 'verbose_name', 'required', 'unique')
    readonly_fields = ('name', 'type', 'verbose_name', 'required', 'unique')


class ModelWrapperRelationInline(admin.TabularInline):
    extra = 0
    max_num = 0
    model = Relation
    can_delete = False
    fk_name = 'model'
    fields = ('name', 'type', 'related_model', 'required', 'unique')
    readonly_fields = ('name', 'type', 'related_model', 'required', 'unique')


class ModelWrapperAdmin(admin.ModelAdmin):
    fields = ('content_type', )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return super(ModelWrapperAdmin, self).get_fieldsets(request, obj)
        return (
            (None, {'fields': ('name', 'db_table')}),
            ('Display', {'fields': ('verbose_name', 'verbose_name_plural'), 'classes': ('collapse', )}),
        )

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return ()
        else:
            return ('content_type', 'name', 'inherits', 'verbose_name', 'verbose_name_plural', 'db_table')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return super(ModelWrapperAdmin, self).get_inline_instances(request, obj)
        return (ModelWrapperFieldInline(self.model, self.admin_site), ModelWrapperRelationInline(self.model, self.admin_site))


admin.site.register(ModelWrapper, ModelWrapperAdmin)

