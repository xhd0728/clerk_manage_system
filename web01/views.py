from django.shortcuts import render, redirect
from web01 import models


# Create your views here.
def depart_list(request):
    """ 部门列表 """

    # 去数据库中获取所有的部门列表
    # [对象，对象，对象……]
    queryset = models.Department.objects.all()

    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    """ 添加部门 """
    if request.method == "GET":
        return render(request, 'depart_add.html')
    # 获取用户POST提交的数据（title输入为空）
    title = request.POST.get("title")

    # 保存到数据库
    models.Department.objects.create(title=title)

    # 重定向回部门列表页面
    return redirect("/depart/list/")


def depart_delete(request):
    """ 删除部门 """
    # URL传参为GET类型
    # 获取id
    nid = request.GET.get('nid')

    # 删除
    models.Department.objects.filter(id=nid).delete()

    # 重定向回部门列表页面
    return redirect("/depart/list/")


def depart_edit(request, nid):
    """ 修改部门 """
    if request.method == "GET":
        # 根据nid获取他的数据
        row_object = models.Department.objects.filter(id=nid).first()

        return render(request, 'depart_edit.html', {"row_object": row_object})

    # 获取用户提交的标题
    title = request.POST.get("title")

    # 根据ID找到数据库中的数据并进行更新
    models.Department.objects.filter(id=nid).update(title=title)

    # 重定向回部门列表
    return redirect("/depart/list/")


def user_list(request):
    """ 用户管理 """

    # 获取所有的用户列表
    queryset = models.UserInfo.objects.all()
    """
    # 用python语法实现
    for obj in queryset:
        print(obj.id, obj.name, obj.account, obj.create_time.strftime("%Y-%m-%d"), obj.get_gender_display(), obj.depart.title)
        # print(obj.name, obj.depart_id)
        # obj.depart_id # 获取数据库中存储的那个字段值
        # obj.depart.title    # 根据id自动去关联的表中获取哪一行数据depart的对象
    """
    return render(request, 'user_list.html', {"queryset": queryset})


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
    models.UserInfo.objects.create(name=name, password=pwd, age=age, account=account, create_time=ctime, gender=gender, depart_id=depart_id)

    # 返回到用户列表页面
    return redirect("/user/list")

