from django.shortcuts import render, HttpResponse


def upload_list(request):
    if request.method == "GET":
        return render(request, 'upload_list.html')

    # print(request.POST)  # 请求体中数据
    # print(request.FILES)  # 发来的文件

    file_object = request.FILES.get("avatar")
    print(file_object.name)  # 文件名
    f = open(file_object.name, mode='wb')

    for chunk in file_object.chunks():
        f.write(chunk)

    f.close()

    return HttpResponse("...")
