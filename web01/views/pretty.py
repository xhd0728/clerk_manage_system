from django.shortcuts import render, redirect
from web01 import models
from web01.utils.form import PrettyModelForm, PrettyEditModelForm


# Create your views here.


def pretty_list(request):
    """ 靓号列表 """

    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile="18822224444", price=10, level=1, status=1)

    # import copy
    # from django.http.request import QueryDict
    # query_dict = copy.deepcopy(request.GET)
    # query_dict._mutable = True
    # query_dict.setlist('page', [11])
    # print(query_dict.urlencode())

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    from web01.utils.pagination import Pagination

    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "search_data": search_data,
        "page_string": page_object.html(),  # 生成的页码
    }

    # res = models.PrettyNum.objects.filter(**data_dict)
    # print(res)

    # 列表
    # q1 = models.PrettyNum.objects.filter(mobile="13622223333", id=2)
    # print(q1)

    # data_dict = {"mobile": "13622223333", "id": 2}
    # q2 = models.PrettyNum.objects.filter(**data_dict)
    # print(q2)

    # select * from 表 order by level desc;

    return render(request, 'pretty_list.html', context)


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
