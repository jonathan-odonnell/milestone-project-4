from functools import wraps
from django.shortcuts import HttpResponse

def superuser_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse(403)
        return function(request, *args, **kwargs)
    return wrap