import json
from django import forms
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from web01.utils.bootstrap import BootStrapModelForm
from web01 import models
from web01.utils.pagination import Pagination


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            # "detail": forms.Textarea
            "detail": forms.TextInput
        }


def task_list(request):
    """ 任务列表 """
    # 去数据库获取所有的任务
    queryset = models.Task.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)
    form = TaskModelForm()
    context = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }
    return render(request, "task_list.html", context)


@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST)
    data_dict = {"status": True, "data": [11, 22, 33, 44]}
    # return HttpResponse(json.dumps(data_dict))

    return JsonResponse(data_dict)


@csrf_exempt
def task_add(request):
    print(request.POST)

    # 1.用户发送过来的数据进行校验（Model Form进行校验）
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status": False, "error": form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
