from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 0.排除那些不需要登录就能访问的页面
        # request.path_info 获取当前用户请求的url /login/
        if request.path_info == "/login/":
            return
        # 如果方法中没有返回值，None
        # 如果有返回值 HttpResponse，render，redirect
        # 1.读取当前访问用户的session信息，如果能读取到，说明已经登陆，继续向后走
        info_dict = request.session.get("info")
        if info_dict:
            return

        # 2.如果没有登录过，回到登录页面
        return redirect('/login/')
