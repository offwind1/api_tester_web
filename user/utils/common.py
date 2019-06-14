from django.db import DataError

from user.models import UserInfo


def add_register_data(**kwargs):
    """
    用户注册信息逻辑判断及落地
    :param kwargs: dict
    :return: ok or tips
    """
    user_info = UserInfo.objects
    try:
        username = kwargs.pop('account')
        password = kwargs.pop('password')
        email = kwargs.pop('email')

        if user_info.filter(username__exact=username).filter(status=1).count() > 0:
            return '该用户名已被注册，请更换用户名'
        if user_info.filter(email__exact=email).filter(status=1).count() > 0:
            return '邮箱已被其他用户注册，请更换邮箱'
        user_info.create(username=username, password=password, email=email)
        return 'ok'
    except DataError:
        return '字段长度超长，请重新编辑'