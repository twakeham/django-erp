from django.contrib import admin
from django.db import models as db

from dynamic.models import Field
from models import *
from forms import ChecklistFieldForm
from widgets import DisabledSelectField


class ChecklistItemAdmin(admin.TabularInline):
    form = ChecklistFieldForm
    model = Field
    extra = 0


class ChecklistAdmin(admin.ModelAdmin):

    list_display = ['name', 'verbose_name']
    inlines = (ChecklistItemAdmin, )

    fieldsets = [
        (None, {'fields': ['name']}),
        ('Display', {'fields': ['verbose_name', 'verbose_name_plural'], 'classes': ('collapse', )}),
        ('Forms', {'fields': ['form', 'followup_form']})
    ]

admin.site.register(Checklist, ChecklistAdmin)
