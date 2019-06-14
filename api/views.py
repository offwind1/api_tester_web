import json

from django.shortcuts import render, render_to_response

from user.views import login_check
# Create your views here.


@login_check
def index(request):
    """
        api测试主页
    """
    data = {
        'account': request.session["now_account"]
    }
    return render_to_response("api_index.html", data)


@login_check
def add_api(request):
    account = request.session["now_account"]

    return render_to_response('add_api.html')


