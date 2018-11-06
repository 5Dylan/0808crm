# -*- coding:utf-8 -*-
from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from system.models import User, UserRole, Role, Permission, Module


class CustomSystemException(Exception):
    """自定义异常类"""

    def __init__(self, code=400, msg='系统错误，请联系管理员'):
        self.code = code
        self.msg = msg

    @staticmethod
    def eroor(msg):
        c = CustomSystemException(msg=msg)
        return c


class CrmExceptionMiddleware(MiddlewareMixin):
    """全局异常处理中间件"""

    def process_exception(self, request, exception):
        # 如果是自定义异常
        if isinstance(exception, CustomSystemException):
            result = Message(code=exception.code, msg=exception.msg).result()
        elif isinstance(exception, Exception) or isinstance(exception, BaseException):
            # 如果是python系统异常
            # 系统出现异常，将异常信息存入数据库或者日志记录文件，方便维护查看
            result = Message(code=400, msg='系统错误，请联系管理员').result()

        # 判断请求是否是ajax
        if request.is_ajax():
            return JsonResponse(result)
        else:
            return render(request, 'error.html', result)


class CrmUrlMiddleware(MiddlewareMixin):
    """全局url拦截中间件"""

    def process_request(self, request):
        # 判断是否是允许访问地址
        urls = ['login_register', 'unique_username', 'unique_email', 'send_email', 'active_accounts', 'login_user']
        url = request.path.split('/')[-2]

        # 没有则重定向至login页面
        if url not in urls:
            # 如果访问路径不存在，判断session中是否有用户信息，有则放行
            username = request.session.get('username_session')
            if not username:
                return redirect('system:login_register')

            try:
                # 删除该用户的权限信息
                del request.session['user_permission']
            except Exception as e:
                pass

            # 根据用户名获取用户
            user = User.objects.get(username=username)
            role_id = user.roles.values_list('id', flat=True).all()
            # 根据角色查询模块
            module_id = Permission.objects.values_list('module', flat=True).filter(role__id__in=role_id)
            # 根据模块获取资源
            opt_value = list(Module.objects.values_list('optValue', flat=True).filter(pk__in=module_id))
            # 根据用户将资源信息添加至session
            request.session['user_permission'] = opt_value
            # 设置session失效时间，关闭浏览器session失效
            request.session.set_expiry(0)


class Message(object):
    """公共返回对象"""

    def __init__(self, code=200, msg='success', obj=None):
        self.code = code,
        self.msg = msg,
        self.obj = obj

    def result(self):
        result = {'code': self.code[0], 'msg': self.msg[0]}
        if self.obj:
            result['obj'] = self.obj[0]
        return result


def permission_required(permission):
    """自定义views的权限校验装饰器"""

    def decorator(func):
        # 权限认证
        def warpper(request, *args, **kwargs):
            """检查是否有权限"""
            user_permission = request.session.get('user_permission')
            if not user_permission or permission not in user_permission:
                raise CustomSystemException.eroor("没有操作权限，请联系管理员")
            else:
                # 当前有用户登录，正常跳转
                return func(request, *args, **kwargs)

        return warpper

    return decorator


def is_empty(value, code=400, msg='系统异常，请联系管理员'):
    """全局非空判断"""
    if value is None:
        raise CustomSystemException(code, msg)


if __name__ == '__main__':
    c = CustomSystemException.eroor("没有操作权限，请联系管理员")
    print(isinstance(c, CustomSystemException))
