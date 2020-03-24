from django.shortcuts import redirect
from User.views import *


def user_login(function):
    def wrap(self, request, *args, **kwargs):
        try:
            if request.session.get('uid'):
                return function(self, request, *args, **kwargs)
            else:
                return redirect("/user/user-login/")
        except Exception as e:
            print(str(e))
            return redirect('/user/user-login/')
    return wrap
