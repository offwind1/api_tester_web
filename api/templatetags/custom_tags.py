import json

from django import template

register = template.Library()



# def update_include(include):
#     for i in range(0, len(include)):
#         if isinstance(include[i], dict):
#             id = include[i]['config'][0]
#             source_name = include[i]['config'][1]
#             try:
#                 name = TestCaseInfo.objects.get(id=id).name
#             except ObjectDoesNotExist:
#                 name = source_name+'_已删除!'
#                 logger.warning('依赖的 {name} 用例/配置已经被删除啦！！'.format(name=source_name))
#
#             include[i] = {
#                 'config': [id, name]
#             }
#         else:
#             id = include[i][0]
#             source_name = include[i][1]
#             try:
#                 name = TestCaseInfo.objects.get(id=id).name
#             except ObjectDoesNotExist:
#                 name = source_name + ' 已删除'
#                 logger.warning('依赖的 {name} 用例/配置已经被删除啦！！'.format(name=source_name))
#
#             include[i] = [id, name]
#
#     return include




@register.filter(name='data_type')
def data_type(value):
    """
    返回数据类型 自建filter
    :param value:
    :return: the type of value
    """
    return str(type(value).__name__)


@register.filter(name='convert_eval')
def convert_eval(value):
    """
    数据eval转换 自建filter
    :param value:
    :return: the value which had been eval
    """
    # return update_include(eval(value))
    return ""


@register.filter(name='json_dumps')
def json_dumps(value):
    return json.dumps(value, indent=4, separators=(',', ': '), ensure_ascii=False)


@register.filter(name='is_del')
def id_del(value):
    if value.endswith('已删除'):
        return True
    else:
        return False



