from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from serve.models import CustomerServe
from django.http import JsonResponse
from crm.common import Message
from datetime import datetime


@require_GET
def serve_index(request, serve_type):
    """服务公共首页跳转"""
    return render(request, 'serve/serve_{}.html'.format(serve_type))


@require_POST
def create_serve(request):
    """创建服务"""
    try:
        # 接收参数
        data = request.POST.dict()
        # 弹出csrfmiddlewaretoken
        data.pop('csrfmiddlewaretoken')
        # 准备数据
        data['state'] = '已创建'
        data['createPeople'] = request.session.get('username_session')

        serviceRequest = data.pop('serviceRequest')
        print(serviceRequest)
        # 创建
        # CustomerServe.objects.create(**data)
        # 返回数据
        return JsonResponse(Message(msg='创建成功').result())
    except Exception as e:
        return JsonResponse(Message(code=400, msg='创建失败').result())


@require_GET
def select_serve(request):
    """查询服务"""
    try:
        # 获取第几页
        page_num = request.GET.get('page', 1)  # 添加默认值，防止没有参数导致的异常错误

        # 获取每页多少条
        page_size = request.GET.get('rows', 10)  # 添加默认值，防止没有参数导致的异常错误

        # 接收参数
        state = request.GET.get('state')

        # 查询
        object_list = CustomerServe.objects.values().filter(state=state).order_by('-id')

        # 已归档的条件查询
        customer = request.GET.get('customer')
        if customer:
            object_list = object_list.filter(customer__icontains=customer)

        overview = request.GET.get('overview')
        if overview:
            object_list = object_list.filter(overview__icontains=overview)

        serveType = request.GET.get('serveType')
        if serveType and '请选择服务类型' != serveType:
            object_list = object_list.filter(serveType=serveType)

        createTimefrom = request.GET.get('createTimefrom')
        if createTimefrom:
            object_list = object_list.filter(createDate__gte=createTimefrom)

        createDateto = request.GET.get('createDateto')
        if createDateto:
            object_list = object_list.filter(createDate__lte=createDateto)

        # 初始化分页对象
        p = Paginator(object_list, page_size)

        # 获取指定页数的数据
        data = p.page(page_num).object_list

        # 返回总条数
        count = p.count

        # 返回数据
        context = {
            'total': count,
            'rows': list(data)
        }
        return JsonResponse(context)
    except CustomerServe.DoesNotExist as e:
        pass


def update_serve(request):
    """修改服务"""
    try:
        # 接收参数
        data = request.POST.dict()
        # 弹出数据
        data.pop('csrfmiddlewaretoken')
        id = data.pop('id')
        # 准备数据
        state = data.get('state')
        # 如果是已分配，已处理，已归档...
        if '已分配' == state:
            data['assignTime'] = datetime.now()

        if '已处理' == state:
            data['serviceProceTime'] = datetime.now()

        data['updateDate'] = datetime.now()
        # 修改
        CustomerServe.objects.filter(pk=id).update(**data)
        # 返回数据
        return JsonResponse(Message(msg='操作成功').result())
    except Exception as e:
        print(e)
        return JsonResponse(Message(code=400, msg='操作失败').result())
