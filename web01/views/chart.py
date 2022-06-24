from django.shortcuts import render


def chart_list(request):
    """ 数据统计页面 """
    return render(request, 'chart_list.html')
