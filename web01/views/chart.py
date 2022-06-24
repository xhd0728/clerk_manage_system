from django.shortcuts import render
from django.http import JsonResponse


def chart_list(request):
    """ 数据统计页面 """
    return render(request, 'chart_list.html')


def chart_bar(request):
    """ 构造柱状图的数据 """
    # 数据可以到数据库中获取
    legend = [
        "销量",
        "业绩",
    ]
    series_list = [
        {
            "name": '销量',
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": '业绩',
            "type": 'bar',
            "data": [13, 10, 26, 11, 7, 10]
        },
    ]
    x_axis = [
        "1月", "2月", "3月", "4月", "5月", "6月",
    ]

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series_list,
            "x_axis": x_axis,
        }
    }
    return JsonResponse(result)


def chart_pie(request):
    """ 构造饼图的数据 """

    db_data_list = [
        {"value": 2048, "name": 'IT部门'},
        {"value": 1735, "name": '运营'},
        {"value": 580, "name": '新媒体'},
    ]

    result = {
        "status": True,
        "data": db_data_list,
    }

    return JsonResponse(result)


def chart_line(request):
    """ 构造折线图的数据 """
    legend = [
        "上海",
        "黑龙江",
    ]
    series_list = [
        {
            "name": '上海',
            "type": 'line',
            "stack": 'Total',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": '黑龙江',
            "type": 'line',
            "stack": 'Total',
            "data": [13, 10, 26, 11, 7, 10]
        },
    ]
    x_axis = [
        "1月", "2月", "3月", "4月", "5月", "6月",
    ]

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series_list,
            "x_axis": x_axis,
        }
    }
    return JsonResponse(result)


def highcharts(request):
    """ highcharts实例 """
    return render(request, 'highcharts.html')
