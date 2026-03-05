from django.http import HttpResponse
from functools import wraps

def staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse("Login required")

        if request.user.profile.role != 'staff':
            return HttpResponse("Unauthorized access")

        return view_func(request, *args, **kwargs)
    return wrapper