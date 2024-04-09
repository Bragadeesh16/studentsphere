from functools import wraps
from django.http import HttpResponseForbidden
from .views import *
from django.shortcuts import render,redirect

def authenticate_users(view_func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('signup') 
    return wrapper

def authenticate_staff(view_func):
    def wrapper(request,*args,**kwargs):
        if (request.user.groups.filter(name='staff').exists() or request.user.is_superuser):
            return view_func(request,*args,**kwargs)
        else:
            return HttpResponseForbidden(request,'your are not allowed')
    return wrapper
