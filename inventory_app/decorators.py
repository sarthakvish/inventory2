from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

from inventory import settings

def login_excluded(redirect_to):
    """ This decorator kicks authenticated users out of a view """
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper


def anonymous_required(function=None, redirect_url=None):

   if not redirect_url:
       redirect_url = settings.LOGIN_REDIRECT_URL

   actual_decorator = user_passes_test(
       lambda u: u.is_anonymous(),
       login_url=redirect_url
   )

   if function:
       return actual_decorator(function)
   return actual_decorator