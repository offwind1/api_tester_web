import json

from django.http import HttpResponse
from django.shortcuts import render, render_to_response

from api.models import Project, Api, Module
from common import set_filter_session, get_module_list
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

    if request.is_ajax():
        # 新增api
        body_str = request.body.decode('utf-8')
        module_info = json.loads(body_str)
        name = module_info.get("test").get("name")

        case_name = name.get("case_name")
        project = name.get('project')
        module = name.get('module')

        if case_name is None:
            return HttpResponse("API名称不能为空")

        if project and module:
            try:
                m = Module.objects.get(id=int(module))
                Api.objects.create(belong_module=m, api_name=case_name, request=body_str)
                return HttpResponse("/api/api_list/")
            except (Module.DoesNotExist, Project.DoesNotExist):
                pass
        return HttpResponse("项目或模块有误")
    else:
        return render_to_response('add_api.html', {
            "project": Project.objects.all().order_by("-create_time"),
            "account": account
        })


@login_check
def api_list(request, id=1):
    account = request.session["now_account"]

    if request.is_ajax():
        # 删除操作
        api_info = json.loads(request.body.decode('utf-8'))
        mode = api_info.get("mode")
        id_ = api_info.get("id")

        if mode and mode == "del" and id_:
            try:
                Api.objects.get(id=id_).delete()
            except Api.DoesNotExist:
                return HttpResponse("删除出错，不存在该api")
        return HttpResponse("ok")
    else:
        filter_query = set_filter_session(request)
        module_list = get_module_list(filter_query, request)

        if request.method == "GET":
            api_list = Api.objects.all().order_by("-create_time")
        elif request.method == "POST":
            name = request.POST.get("name")
            if module_list:
                api_list = []
                for module in module_list:
                    apis = Api.objects.filter(belong_module=module, api_name__contains=name).order_by("-create_time")
                    api_list = api_list + list(apis)
            else:
                api_list = Api.objects.all().order_by("-create_time")

    manage_info = {
        'account': account,
        'project_menu': Project.objects.all().order_by('-create_time'),
        "module_list": module_list,
        "api_list": api_list,
    }
    manage_info.update(filter_query)

    return render_to_response('api_list.html', manage_info)


def edit_api(request, id=None):
    if id is None:
        id = ""

    account = request.session["now_account"]

    if request.is_ajax():
        body_str = request.body.decode('utf-8')
        module_info = json.loads(body_str)
        name = module_info.get("test").get("name")

        case_name = name.get("case_name")
        project = name.get('project')
        module = name.get('module')

        if case_name is None:
            return HttpResponse("API名称不能为空")

        if project and module:
            try:
                m = Module.objects.get(id=int(module))
                msg = Api.objects.update(m, case_name, body_str, id)
                return HttpResponse(msg)
            except (Module.DoesNotExist, Project.DoesNotExist):
                pass
        return HttpResponse("项目或模块有误")

    api = Api.objects.filter(id=id).first()
    if api:
        req = eval(api.request)
        req = req['test']
    else:
        req = ""

    manage_info = {
        'account': account,
        'api': api,
        'request': req,
        'project': Project.objects.all().values('project_name').order_by('-create_time'),
        'id': id,
    }

    return render_to_response('edit_api.html', manage_info)


def get_api(request):
    module_info = json.loads(request.body.decode('utf-8'))
    print(module_info)
    module = module_info.get("module")

    if not module:
        return HttpResponse("error! 项目参数有误")

    if module == "All" or module == "请选择":
        return HttpResponse("")

    api_set = Module.objects.get(id=module).api_set.all()

    string = ''
    for api in api_set:
        string = string + str(api.id) + '^=' + api.api_name + 'replaceFlag'
    return HttpResponse(string[:len(string) - 11])



def add_case(request, id=1):
    account = request.session["now_account"]
    filter_query = set_filter_session(request)

    manage_info = {
        'account': account,
        'project': Project.objects.all().order_by('-create_time'),
    }
    manage_info.update(filter_query)

    return render_to_response('add_case.html', manage_info)





