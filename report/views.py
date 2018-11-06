from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from customer.models import Customer
from serve.models import CustomerServe


@require_GET
def contirbute_index(request):
    """客户贡献分析首页"""
    return render(request, 'report/contribute.html')


@require_GET
def select_contirbute(request):
    """查询客户贡献"""
    try:
        '''
        SELECT c.id, c.name, sum(od.sum) sum FROM t_customer c
        LEFT JOIN t_customer_order co ON c.id = co.cus_id
        LEFT JOIN t_order_details od ON co.id = od.order_id
        WHERE c.is_valid = 1 AND c.id = 1 GROUP BY c.id, c.name;
        '''
        # 获取第几页
        page_num = request.GET.get('page', 1)  # 添加默认值，防止没有参数导致的异常错误

        # 获取每页多少条
        page_size = request.GET.get('rows', 10)  # 添加默认值，防止没有参数导致的异常错误

        object_list = Customer.objects.values('id', 'name').annotate(
            sum=Sum('customerorders__ordersdetail__sum')).order_by('-sum')

        # 接收参数
        name = request.GET.get('name')
        if name:
            object_list = object_list.filter(name__icontains=name)

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
def composition_index(request):
    """客户构成分析首页"""
    return render(request, 'report/composition.html')


@require_GET
def select_compostion(request):
    """查询客户构成数据"""
    level = Customer.objects.values('level').annotate(amount=Count('level')).order_by('level')
    return JsonResponse(list(level), safe=False)


@require_GET
def serve_index(request):
    """客户服务分析首页"""
    return render(request, 'report/serve.html')


@require_GET
def select_serve(request):
    """查询客户服务类型数据"""
    serve = CustomerServe.objects.values('serveType').annotate(amount=Count('serveType')).order_by('serveType')
    return JsonResponse(list(serve), safe=False)


@require_GET
def loss_index(request):
    """客户流失分析首页"""
    return render(request, 'report/report_loss.html')
