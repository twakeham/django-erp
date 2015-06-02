from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.utils import importlib

class Command(NoArgsCommand):
    help = "Install all ERP apps"
    def handle_noargs(self, **options):
        for app in settings.INSTALLED_APPS:
            try:
                importlib.import_module('{0}.install'.format(app))
            except:
                continue
            print 'Installed {0}'.format(app)