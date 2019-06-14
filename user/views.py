import json

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response

from user.utils.common import *
from common import *


def login_check(func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('login_status'):
            return HttpResponseRedirect('/user/login/')
        return func(request, *args, **kwargs)

    return wrapper


def login_views(request):
    return render(request, "login.html")


def login(request):
    if request.method == 'POST':
        username = request.POST.get('account')
        password = request.POST.get('password')

        if UserInfo.objects.filter(username__exact=username).filter(password__exact=password).count() == 1:
            request.session["login_status"] = True
            request.session["now_account"] = username
            return HttpResponseRedirect('/api/index/')
        else:
            request.session["login_status"] = False
            return render_to_response("login.html")
    elif request.method == 'GET':
        return render_to_response("login.html")


def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.is_ajax():
        user_info = json.loads(request.body.decode('utf-8'))
        msg = add_register_data(**user_info)
        return HttpResponse(
            get_ajax_msg(msg, '恭喜您，账号已成功注册')
        )
    elif request.method == 'GET':
        return render_to_response("register.html")
