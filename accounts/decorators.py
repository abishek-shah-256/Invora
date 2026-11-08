from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not request.user.is_invora_admin:
            raise PermissionDenied("Only Invora administrators can access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped

def role_required(*role_codes):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            if request.user.is_invora_admin or request.user.role_code in role_codes:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied("You do not have permission to perform this action.")
        return _wrapped
    return decorator
