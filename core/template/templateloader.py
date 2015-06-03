from django.template.loader import BaseLoader
from django.template.base import TemplateDoesNotExist

from models import Template


class DatabaseTemplateLoader(BaseLoader):

    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        try:
            template = Template.objects.get(pk=template_name)
        except Template.DoesNotExist:
            raise TemplateDoesNotExist

        return (template.template, template_name)




