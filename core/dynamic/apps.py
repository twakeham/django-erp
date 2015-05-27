from django.apps import AppConfig


class DynamicModelApp(AppConfig):
    name = 'core.dynamic'
    verbose_name = 'Data types'


class UDTModelApp(AppConfig):
    name = 'core.udt'
    verbose_name = 'User data types'

