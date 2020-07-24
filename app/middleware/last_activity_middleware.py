from core.models import User
from django.utils import timezone


class LastActivityMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        User.objects.filter(id=request.user.pk).update(
                last_activity=timezone.now())
        return response


