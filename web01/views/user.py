from django.shortcuts import render, redirect
from web01 import models
from web01.utils.pagination import Pagination
from web01.utils.form import UserModelForm


# Create your views here.


def user_list(request):
    """ 用户管理 """

    # 获取所有的用户列表
    queryset = models.UserInfo.objects.all()

    page_object = Pagination(request, queryset, page_size=10)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }

    """
    # 用python语法实现
    for obj in queryset:
        print(obj.id, obj.name, obj.account, obj.create_time.strftime("%Y-%m-%d"), obj.get_gender_display(), obj.depart.title)
        # print(obj.name, obj.depart_id)
        # obj.depart_id # 获取数据库中存储的那个字段值
        # obj.depart.title    # 根据id自动去关联的表中获取哪一行数据depart的对象
    """
    return render(request, 'user_list.html', context)


def user_add(request):
    """ 添加用户（原始方式） """
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all(),
        }
        return render(request, 'user_add.html', context)

    # 获取用户提交的数据
    name = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender = request.POST.get('gd')
    depart_id = request.POST.get('dp')

    # 添加到数据库中
    models.UserInfo.objects.create(name=name, password=pwd, age=age, account=account, create_time=ctime, gender=gender,
                                   depart_id=depart_id)

    # 返回到用户列表页面
    return redirect("/user/list")


def user_model_form_add(request):
    """ 添加用户 """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})

    # 用户通过POST提交数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        # print(form.cleaned_data)
        form.save()
        return redirect('/user/list/')
    # 校验失败（在页面上显示错误信息）
    return render(request, "user_model_form_add.html", {"form": form})


def user_edit(request, nid):
    """ 编辑用户 """
    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据

        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {"form": form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据
        # 增加值，额外添加
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')

    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')
