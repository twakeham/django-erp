from django.apps import AppConfig

from core.form.signals import form_pre_save


class UserApp(AppConfig):
    name = 'apps.user'
    verbose_name = 'User Authentication'


