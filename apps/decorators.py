from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from apps.utils import get_default_param

__author__ = 'aamish'


def my_login_required(f):
    def wrap(request, *args, **kwargs):
        # token = get_default_param(request, 'token', None)
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if token:
            auth = Token.objects.filter(key=token).first()
            if auth:
                return f(request, auth.user, *args, **kwargs)
            return Response({"message": "User not Authenticated"})
        return Response({"message": "Authentication is Required"})
    return wrap