
from django.shortcuts import redirect

from django.contrib import messages

def signin_requred(fn):

    def wrapper(request,*args,**kwargs):

        if not request.user.is_authenticated:

            messages.error(request,"invalid session please login")

            return redirect("sighnin")
        
        else:

            return fn(request,*args,**kwargs)
        
    return wrapper
