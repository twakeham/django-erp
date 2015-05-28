from django import forms

from dynamic.models import Field, BOOLEAN, FIELD_CHOICES


class ChecklistFieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ('type', 'name', 'verbose_name', 'help_text', 'sort_order')

    def __init__(self, *args, **kwargs):
        super(ChecklistFieldForm, self).__init__(*args, **kwargs)
        self.fields['type'].initial = BOOLEAN
        self.fields['type'].choices = FIELD_CHOICES