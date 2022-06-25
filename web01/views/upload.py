from django.shortcuts import render, HttpResponse
from django import forms
from web01.utils.bootstrap import BootStrapForm, BootStrapModelForm
from web01 import models
from django.conf import settings
import os


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


class UpForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']
    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")


def upload_form(request):
    title = "Form上传"
    if request.method == "GET":
        form = UpForm()
        return render(request, 'upload_form.html', {"form": form, "title": title})

    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # print(form.cleaned_data)
        # 读取到内容，自己处理每个字段的数据
        # 1.读取图片内容，写入到文件夹中，并获取文件的路径
        image_object = form.cleaned_data.get("img")
        # file_path = "web01/static/img/{}".format(image_object.name)
        # media_path = os.path.join(settings.MEDIA_ROOT, image_object.name)
        media_path = os.path.join("media", image_object.name)
        f = open(media_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()

        # 2.将文件的路径写入到数据库中
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=media_path,
        )

        return HttpResponse("...")

    return render(request, 'upload_form.html', {"form": form, "title": title})


class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.City
        fields = "__all__"


def upload_model_form(request):
    """ 上传文件和数据（ModelForm） """
    title = "ModelForm上传文件"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form": form, "title": title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对于文件：自动保存
        # 字段 + 上传路径写入数据库
        form.save()
        return HttpResponse("success!")

    return render(request, 'upload_form.html', {"form": form, "title": title})
