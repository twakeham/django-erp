from django.db.models import signals
from django.utils.functional import curry

from core.user.fields import UserField


class UserLoggingMiddleware(object):
    def process_request(self, request):
        if not request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            if hasattr(request, 'user') and request.user.is_authenticated():
                user = request.user

            else:
                user = None

            session = request.session.session_key

            update_pre_save_info = curry(self._update_pre_save_info, user, session)
            signals.pre_save.connect(update_pre_save_info,  dispatch_uid=(self.__class__, request,), weak=False)

    def process_response(self, request, response):
        signals.pre_save.disconnect(dispatch_uid=(self.__class__, request,))
        signals.post_save.disconnect(dispatch_uid=(self.__class__, request,))
        return response


    def _update_pre_save_info(self, user, session, sender, instance, **kwargs):

        if not sender._meta.app_label == 'udt':
            return

        model = sender
        for field in model._meta.fields:
            if isinstance(field, UserField):
                setattr(instance, field.name, user)

