from django.core.paginator import Paginator
from django.shortcuts import render
from base.models import DataDic, Product
from django.views.decorators.http import require_GET, require_POST
from django.http import JsonResponse
from datetime import datetime
from crm.common import Message


@require_GET
def select_customer_level(request):
    """查询数据字典根据字典名查字典值"""
    try:
        # 接收参数
        dic_name = request.GET.get('dic_name')
        # 查询
        d = DataDic.objects.values('dataDicValue').filter(dataDicName=dic_name).all()
        # 返回数据
        return JsonResponse(list(d), safe=False)
    except Exception as e:
        return JsonResponse({'code': 400, 'msg': 'error'})


def datadic_index(request):
    """数据字典管理首页"""
    return render(request, 'base/datadic_index.html')


@require_GET
def select_datadic(request):
    """查询所有数据字典"""
    try:
        # 获取第几页
        page_num = request.GET.get('page', 1)  # 添加默认值，防止没有参数导致的异常错误

        # 获取每页多少条
        page_size = request.GET.get('rows', 10)  # 添加默认值，防止没有参数导致的异常错误

        object_list = DataDic.objects.values().all()

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
    except Exception as e:
        pass


@require_GET
def select_datadic_name(request):
    """查询数据字典名称"""
    try:
        # 查询
        dataDicName = DataDic.objects.values('dataDicName').distinct().all().order_by('dataDicName')
        # 返回数据
        return JsonResponse(list(dataDicName), safe=False)
    except DataDic.DoesNotExist as e:
        pass


@require_POST
def create_datadic(request):
    """添加数据字典"""
    # 接收参数
    dataDicName = request.POST.get('dataDicName')
    dataDicValue = request.POST.get('dataDicValue')

    DataDic.objects.create(dataDicName=dataDicName, dataDicValue=dataDicValue)
    return JsonResponse(Message(msg='添加成功').result())


@require_POST
def update_datadic(request):
    """修改数据字典"""
    # 接收参数
    id = request.POST.get('id')
    dataDicName = request.POST.get('dataDicName')
    dataDicValue = request.POST.get('dataDicValue')

    DataDic.objects.filter(pk=id).update(dataDicName=dataDicName, dataDicValue=dataDicValue,
                                         updateDate=datetime.now())
    return JsonResponse(Message(msg='修改成功').result())


@require_GET
def delete_datadic(request):
    """删除数据字典"""
    # 接收参数
    ids = request.GET.get('id')
    ids = ids.split(',')
    # 逻辑删除
    DataDic.objects.filter(pk__in=ids).update(isValid=0, updateDate=datetime.now())
    return JsonResponse(Message(msg='删除成功').result())


def product_index(request):
    """产品信息管理首页"""
    return render(request, 'base/product_index.html')


@require_GET
def select_product(request):
    """查询所有产品信息"""
    try:
        # 获取第几页
        page_num = request.GET.get('page', 1)  # 添加默认值，防止没有参数导致的异常错误

        # 获取每页多少条
        page_size = request.GET.get('rows', 10)  # 添加默认值，防止没有参数导致的异常错误

        object_list = Product.objects.values().all().order_by('-id')

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
    except Exception as e:
        pass


@require_POST
def create_product(request):
    """添加产品信息"""
    data = request.POST.dict()
    # 弹出csrfmiddlewaretoken
    data.pop('csrfmiddlewaretoken')
    # 弹出id
    pk = data.pop('id')
    # 添加
    Product.objects.create(**data)
    return JsonResponse({'code': 200, 'msg': '添加成功'})


@require_POST
def update_product(request):
    """修改产品信息"""
    data = request.POST.dict()
    # 弹出csrfmiddlewaretoken
    data.pop('csrfmiddlewaretoken')
    # 弹出id
    pk = data.pop('id')
    # 修改数据
    data['updateDate'] = datetime.now()
    Product.objects.filter(pk=pk).update(**data)
    return JsonResponse({'code': 200, 'msg': '修改成功'})


@require_GET
def delete_product(request):
    """删除产品信息"""
    # 接收参数
    ids = request.GET.get('id')
    # 逻辑删除
    Product.objects.filter(pk__in=ids.split(',')).update(isValid=0, updateDate=datetime.now())
    return JsonResponse(Message(msg='删除成功').result())
