from django.shortcuts import render
from web01 import models
from web01.utils.pagination import Pagination


def admin_list(request):
    """ 管理员列表 """

    # 搜索
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["username__contains"] = search_data

    # 根据搜索条件去数据库获取
    queryset = models.Admin.objects.filter(**data_dict)
    page_object = Pagination(request, queryset)

    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'search_data': search_data
    }

    return render(request, 'admin_list.html', context)
