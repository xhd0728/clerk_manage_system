from django.shortcuts import render
import random
from datetime import datetime
from django.http import JsonResponse
from web01.utils.bootstrap import BootStrapModelForm
from web01 import models
from django.views.decorators.csrf import csrf_exempt
from web01.utils.pagination import Pagination


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        # fields = [""]
        exclude = ["oid", "admin"]


def order_list(request):
    queryset = models.Order.objects.all().order_by("-id")
    page_object = Pagination(request, queryset)
    form = OrderModelForm()
    context = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }

    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """ 新建订单(Ajax) """
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # title=？ price=? status=? admin_id=?
        # oid

        # 订单号：额外增加一些不是用户输入的值（自己计算出来的）
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))

        # 管理员

        # form.instance.admin_id 当前登录系统的管理员的ID
        form.instance.admin_id = request.session["info"]["id"]

        # 保存到数据库中
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors})


def order_delete(request):
    """ 删除订单 """
    uid = request.GET.get('uid')
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, "error": "删除失败，数据不存在"})

    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    """ 根据ID获取订单详细 """
    # 方式1
    """
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "error": "数据不存在"})

    # 从数据库获取到一个对象 row_object
    result = {
        "status": True,
        "data": {
            "title": row_object.title,
            "price": row_object.price,
            "status": row_object.status,
        }

    }

    return JsonResponse({"status": True, "data": result})
    """

    # 方式2
    uid = request.GET.get("uid")
    row_dict = models.Order.objects.filter(id=uid).values("title", "price", "status").first()
    if not row_dict:
        return JsonResponse({"status": False, "error": "数据不存在"})

    # 从数据库获取到一个对象 row_object
    result = {
        "status": True,
        "data": row_dict,
    }
    return JsonResponse(result)
