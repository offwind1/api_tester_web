from api.models import Module, Api


def get_ajax_msg(msg, success):
    """
    ajax提示信息
    :param msg: str：msg
    :param success: str：
    :return:
    """
    return success if msg is 'ok' else msg


def set_filter_session(request):
    """
    update session
    :param request:
    :return:
    """
    if request.method == "POST":
        method_info = request.POST
    else:
        method_info = request.GET

    if 'project' in method_info.keys():
        request.session['project'] = method_info.get('project')
    else:
        request.session['project'] = "All"

    if 'module' in method_info.keys():
        try:
            request.session['module'] = Module.objects.get(id=method_info.get('module')).module_name
        except Exception:
            request.session['module'] = method_info.get('module')

    filter_query = {
        'belong_project': request.session.get("project", ""),
        'belong_module': request.session.get("module", ""),
    }

    return filter_query


def get_module_by_POST(request):
    project = request.POST.get("project")
    module = request.POST.get("module")

    if project and project != "All":
        module_list = get_module_list_by_project_module(project, module)
    else:
        module_list = Module.objects.all().order_by("-create_time")

    return module_list


def get_module_list(filter_query, request):
    if request.method == "GET":
        project = filter_query.get("belong_project")

        if project == "All" or project is None:
            module_list = Module.objects.all().order_by("-create_time")
        else:
            module_list = Module.objects.filter(belong_project__project_name=project).order_by("-create_time")
    elif request.method == "POST":
        module_list = get_module_by_POST(request)
    return module_list


def get_module_list_by_project_module(project, module):
    if module and module != "请选择":
        module_list = Module.objects.filter(belong_project__project_name=project, id=module).order_by(
            "-create_time")
    else:
        module_list = Module.objects.filter(belong_project__project_name=project).order_by("-create_time")
    return module_list
