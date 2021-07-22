from functools import wraps
from django.core.exceptions import PermissionDenied


def superuser_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        """
        A wrap to prevent standard users from accessing the page. Code for
        returning the permission denied exception is from
        https://docs.djangoproject.com/en/3.2/ref/views/#the-403-http-forbidden-view
        """
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return wrap
