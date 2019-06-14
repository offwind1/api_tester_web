import json

from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from api.models import Project, Module
from common import get_ajax_msg, set_filter_session
from user.views import login_check


@login_check
def project_list(request, id=1):
    account = request.session["now_account"]

    if request.is_ajax():
        # 处理删除
        project_info = json.loads(request.body.decode('utf-8'))
        mode = project_info.get("mode")
        id_ = project_info.get("id")

        if mode and mode == "del" and id_:
            try:
                Project.objects.get(id=id_).delete()
            except Project.DoesNotExist:
                return HttpResponse("删除出错，不存在该项目")

        return HttpResponse("ok")

    else:
        # 下拉菜单的项目列表
        project_all = Project.objects.all().order_by('-update_time')

        if request.method == "POST":
            project = request.POST.get("project")
            if project and not project == "All":
                project_list = Project.objects.filter(project_name=project).order_by('-update_time')
            else:
                project_list = Project.objects.all().order_by('-update_time')
        else:
            # 显示的菜单列表
            project_list = project_all

        filter_query = set_filter_session(request)
        manage_info = {
            'account': account,
            'project_all': project_all,
            "project_list": project_list
        }
        manage_info.update(filter_query)
        return render_to_response('project_list.html', manage_info)


@login_check
def add_project(request, id=1):
    account = request.session["now_account"]
    if request.is_ajax():
        project_info = json.loads(request.body.decode('utf-8'))
        project_name = project_info.get("project_name")

        if not project_name:
            return HttpResponse("项目名称不能为空！")

        if Project.objects.filter(project_name=project_name).count() > 0:
            return HttpResponse("项目名称已经存在")

        Project.objects.create(project_name=project_name)
        return HttpResponse('ok')
    elif request.method == 'GET':
        return render_to_response('add_project.html', {
            'account': account
        })


@login_check
def module_list(request, id):
    account = request.session["now_account"]

    if request.is_ajax():
        "删除逻辑"
        project_info = json.loads(request.body.decode('utf-8'))
        mode = project_info.get("mode")
        id_ = project_info.get("id")

        if mode and mode == "del" and id_:
            try:
                Module.objects.get(id=id_).delete()
            except:
                return HttpResponse("删除出错，不存在该模块")

        return HttpResponse("ok")
    else:

        filter_query = set_filter_session(request)

        if request.method == "GET":
            project = filter_query.get("belong_project")

            if project == "All" or project is None:
                module_list = Module.objects.all().order_by("-create_time")
            else:
                module_list = Module.objects.filter(belong_project__project_name=project).order_by("-create_time")

        elif request.method == "POST":
            project = request.POST.get("project")
            module = request.POST.get("module")

            if project and project != "All":
                if module and module != "请选择":

                    module_list = Module.objects.filter(belong_project__project_name=project, id=module).order_by(
                        "-create_time")
                else:
                    module_list = Module.objects.filter(belong_project__project_name=project).order_by("-create_time")
            else:
                module_list = Module.objects.all().order_by("-create_time")

        manage_info = {
            'account': account,
            'project_menu': Project.objects.all().order_by('-create_time'),
            "module_list": module_list,
        }
        manage_info.update(filter_query)

        return render_to_response('module_list.html', manage_info)


@login_check
def add_module(request):
    account = request.session["now_account"]
    if request.is_ajax():
        module_info = json.loads(request.body.decode('utf-8'))
        belong_project = module_info.get("belong_project")
        module_name = module_info.get("module_name")

        try:
            project = Project.objects.get(project_name=belong_project)
        except Project.DoesNotExist:
            return HttpResponse("请选择项目！")

        if module_name:
            Module.objects.create(module_name=module_name, belong_project=project)
        else:
            return HttpResponse("项目名不能为空")
        return HttpResponse("ok")
    elif request.method == 'GET':
        manage_info = {
            'account': account,
            'data': Project.objects.all().values('project_name')
        }
        return render_to_response('add_module.html', manage_info)


def get_module(request):
    module_info = json.loads(request.body.decode('utf-8'))
    project = module_info.get("project")

    if project is None:
        return HttpResponse("error! 项目参数有误")

    if project == "All":
        return HttpResponse("")

    module_set = Project.objects.get(project_name=project).module_set.all()
    string = ''
    for module in module_set:
        string = string + str(module.id) + '^=' + module.module_name + 'replaceFlag'

    return HttpResponse(string[:len(string) - 11])













