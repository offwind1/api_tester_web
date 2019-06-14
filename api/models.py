from django.db import models


# Create your models here.
from api.managers import ApiManager


class BaseTable(models.Model):
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True
        verbose_name = "公共字段表"
        db_table = 'BaseTable'


class Project(BaseTable):
    """项目"""
    project_name = models.CharField("项目名称", max_length=30, unique=True)

    class Meta:
        verbose_name = '项目信息'
        db_table = 'Project'


class Module(BaseTable):
    """模块"""
    module_name = models.CharField("模块名称", max_length=30)
    # 项目外键
    belong_project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '模块信息'
        db_table = 'Module'


class Api(BaseTable):
    """接口"""
    # 接口名称
    api_name = models.CharField("接口名称", max_length=30)
    # 模块外键
    # belong_project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    belong_module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True)
    # 接口模板内容
    request = models.TextField("请求信息")

    objects = ApiManager()

    class Meta:
        verbose_name = '接口'
        db_table = 'Api'




class Step(BaseTable):
    """步骤"""
    step_name = models.CharField("步骤名称", max_length=30)
    # 接口外键
    belong_api = models.ForeignKey(Api, on_delete=models.CASCADE, null=True)
    # 模块外键
    belong_module = models.ForeignKey(Module, on_delete=models.CASCADE)
    # 请求内容
    request = models.TextField("请求信息")

    class Meta:
        verbose_name = '步骤'
        db_table = 'Step'


class Case(BaseTable):
    """用例"""
    # 用例名称
    case_name = models.CharField("用例名称", max_length=30)
    # 模块外键
    belong_module = models.ForeignKey(Module, on_delete=models.CASCADE)
    # 步骤集合 有顺序
    step_list = models.TextField("步骤顺序")

    class Meta:
        verbose_name = '用例'
        db_table = 'Case'


def list1_diff_list2(list1, list2):
    sa = set(list1).difference(set(list2))
    return list(sa)


def eval_str(data):
    try:
        obj = eval(data)
        if obj and isinstance(obj, list):
            return obj
    except Exception:
        pass

    return


def set_caes(case_id, case_name, step_list, mod_id):
    now_step_list = []

    try:
        case = Case.objects.get(id=case_id)
        # 获取曾经的 step_list
        now_step_list = eval_str(case.step_list)

        # 更新step_list
        case.step_list = str(step_list)
        case.case_name = case_name
        case.save()

    except Case.DoesNotExist:
        # 创建 新的用例，并且传递进入的step_list参数，赋予新用例
        Case.objects.create(case_name=case_name, belong_module_id=mod_id, step_list=str(step_list))

    # 获取曾经的step 和 当前的step有什么不同
    diff_list = list1_diff_list2(now_step_list, step_list)

    # 将替换掉的step删除
    for step_id in diff_list:
        step = Step.objects.get(id=step_id)
        step.delete()


class Suite(BaseTable):
    """集合"""
    suite_name = models.CharField("集合名称", max_length=30, unique=True)
    belong_module = models.ForeignKey(Module, on_delete=models.CASCADE)
    case_list = models.TextField("用例集合")

    class Meta:
        verbose_name = '集合'
        db_table = 'Suite'
