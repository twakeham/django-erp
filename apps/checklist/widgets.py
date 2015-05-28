import django.forms as forms
from django.utils.safestring import mark_safe


class DisabledSelectField(forms.Select):
    def render(self, name, value, attrs=None, choices=()):
        attrs.update({
            'disabled': True,
            'style': "color: red;"
        })
        return super(DisabledSelectField, self).render(name, value, {'disabled': True}, choices)