from django.core.validators import RegexValidator, ValidationError
from django.shortcuts import render, redirect
from web01 import models
from django import forms
from django.utils.safestring import mark_safe


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
    models.UserInfo.objects.create(name=name, password=pwd, age=age, account=account, create_time=ctime, gender=gender,
                                   depart_id=depart_id)

    # 返回到用户列表页面
    return redirect("/user/list")


# Model Form实例


class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3, label="用户名")

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有的插件，添加class
        for name, field in self.fields.items():
            # if name == "password":
            #     continue
            # print(name, field)
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


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


def pretty_list(request):
    """ 靓号列表 """

    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile="18822224444", price=10, level=1, status=1)

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    # res = models.PrettyNum.objects.filter(**data_dict)
    # print(res)

    # 列表
    # q1 = models.PrettyNum.objects.filter(mobile="13622223333", id=2)
    # print(q1)

    # data_dict = {"mobile": "13622223333", "id": 2}
    # q2 = models.PrettyNum.objects.filter(**data_dict)
    # print(q2)

    # select * from 表 order by level desc;

    # 根据用户想要访问的页码，计算出起止位置
    page = int(request.GET.get('page', 1))
    page_size = 10
    start = (page - 1) * page_size
    end = page * page_size

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")[start:end]

    # 数据总条数
    total_count = models.PrettyNum.objects.filter(**data_dict).order_by("-level").count()

    # 计算总页码
    total_page_count, div = divmod(total_count, page_size)
    if div:
        total_page_count += 1

    # 计算出显示当前页的前5页，后五页
    plus = 5

    if total_page_count <= 2 * plus + 1:
        # 数据库中的数据比较少，没有达到11页
        start_page = 1
        end_page = total_page_count
    else:
        # 数据库的数据比较多，大于11页
        if page <= plus:
            start_page = 1
            end_page = 2 * plus + 1
        else:
            if (page + plus) > total_page_count:
                start_page = total_page_count - 2 * plus
                end_page = total_page_count
            else:
                start_page = page - plus
                end_page = page + plus

    # 页码
    page_str_list = []

    # 首页
    page_str_list.append('<li><a href="/pretty/list/?page={}">首页</a></li>'.format(1))

    # 上一页
    if page > 1:
        prev = '<li><a href="/pretty/list/?page={}">上一页</a></li>'.format(page - 1)
    else:
        prev = '<li><a href="/pretty/list/?page={}">上一页</a></li>'.format(1)
    page_str_list.append(prev)


    # 页面
    for i in range(start_page, end_page + 1):
        if i == page:
            ele = '<li class="active"><a href="/pretty/list/?page={}">{}</a></li>'.format(i, i)

        else:
            ele = '<li><a href="/pretty/list/?page={}">{}</a></li>'.format(i, i)

        page_str_list.append(ele)

    # 下一页
    if page < total_page_count:
        aftv = '<li><a href="/pretty/list/?page={}">下一页</a></li>'.format(page + 1)
    else:
        aftv = '<li><a href="/pretty/list/?page={}">下一页</a></li>'.format(total_page_count)
    page_str_list.append(aftv)

    # 尾页
    page_str_list.append('<li><a href="/pretty/list/?page={}">尾页</a></li>'.format(total_page_count))

    """
    <li><a href="/pretty/list/?page=1">1</a></li>
    <li><a href="/pretty/list/?page=2">2</a></li>
    <li><a href="/pretty/list/?page=3">3</a></li>
    <li><a href="/pretty/list/?page=4">4</a></li>
    <li><a href="/pretty/list/?page=5">5</a></li>
    """
    page_string = mark_safe("".join(page_str_list))

    return render(request, 'pretty_list.html',
                  {"queryset": queryset, "search_data": search_data, "page_string": page_string})


class PrettyModelForm(forms.ModelForm):
    # 方式1
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    # )

    class Meta:
        model = models.PrettyNum
        # fields = "__all__"
        fields = ["mobile", "price", "level", "status"]
        # exclude = ["level"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # 方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已经存在")

        # 验证通过，用户输入的值返回
        return txt_mobile


def pretty_add(request):
    """ 添加靓号 """
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {"form": form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request, 'pretty_add.html', {"form": form})


class PrettyEditModelForm(forms.ModelForm):
    # mobile = forms.CharField(disabled=True, label="手机号")
    # 方式1
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # 方式2
    def clean_mobile(self):

        # 当前编辑的那一行的ID
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已经存在")

        # 验证通过，用户输入的值返回
        return txt_mobile


def pretty_edit(request, nid):
    """ 编辑靓号 """
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'pretty_edit.html', {"form": form})

    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request, 'pretty_edit.html', {"form": form})


def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')
