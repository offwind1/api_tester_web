from api.models import Module


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
