from django.contrib import admin

from models import Template


class TemplateAdmin(admin.ModelAdmin):

    pass

admin.site.register(Template, TemplateAdmin)
