from django.shortcuts import redirect


def admin_login(function):
    # print(function.__name__)
    def wrap(self, request, *args, **kwargs):
        if request.session.get('admin'):
            # print(request.session.get('admin', None))
            return function(self, request, *args, **kwargs)
        else:
            return redirect('/admingui/admin-login/')
    return wrap
