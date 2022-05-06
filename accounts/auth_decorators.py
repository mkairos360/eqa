from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect


def only_admins(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_qasa:
                return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('401 Unauthorized: You are not authorised to view this page.', status=401)

    return wrapper_func


def allowed_groups(permitted_groups=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group in permitted_groups:
                    return view_func(request, *args, **kwargs)
                if group == 'qasa':
                    return redirect('analytic_dashboard')
                elif group == 'student':
                    return redirect('evaluations')
                else:
                    return HttpResponse('401 Unauthorized: You are not authorised to view this page.', status=401)
            else:
                return HttpResponse('401 Unauthorized: You are not authorised to view this page.', status=401)

        return wrapper_func

    return decorator