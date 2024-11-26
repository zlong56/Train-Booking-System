from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import AnonymousUser

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin or request.user.is_superuser:
                return redirect('adminhome')
            elif request.user.AccType == "Client":
                return redirect('clienthome')
            else:
                return redirect('userhome')
            
        return view_func(request, *args, **kwargs)
    
    return wrapper_func

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.is_superuser or request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("login_user")
    return wrapper_function

def client_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.AccType == "Client":
            return view_func(request, *args, **kwargs)
        else:
            return redirect("login_user")
    return wrapper_function

def superuser_required(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("login_user")
    return wrapper_function