from django.shortcuts import render
from customer.models import Customer, LinkMan, Contact, CustomerOrders, OrdersDetail, CustomerLoss, CustomerReprieve
from system.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator
from crm.common import Message, permission_required
from random import randint
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache


# -----------------------------------客户信息管理-------------------start-------------------
# 查询客户名称和客户联系人名称和用户名称
@require_GET
@permission_required('101001')
def select_cname_and_lname_and_uname(request):
    try:
        # 查询客户
        c = Customer.objects.values('id', 'name').all()

        # 查询联系人
        l = LinkMan.objects.values('id', 'linkName').all()

        # 查询用户(指派人)
        u = User.objects.values('id', 'username').all()

        # 返回数据
        context = {
            'code': 200,
            'msg': 'success',
            'cs': list(c),
            'ls': list(l),
            'us': list(u)
        }
        return JsonResponse(context)
    except ObjectDoesNotExist as e:
        print(e)
        return JsonResponse({'code': 400, 'msg': 'error'})


# 根据联系人主键查询联系电话
def select_link_phone_by_id(request):
    try:
        # 接受参数
        id = request.GET.get('id')

        # 查询联系电话
        lm = LinkMan.objects.get(pk=id)

        # 返回数据
        return JsonResponse({'code': 200, 'msg': 'success', 'phone': lm.phone})
    except LinkMan.DoesNotExist as e:
        return JsonResponse({'code': 400, 'msg': 'error'})


def customer_index(request):
    """跳转客户信息管理首页"""
    return render(request, 'customer/customer.html')


@require_GET
def select_customer_list(request):
    """查询客户信息列表"""
    try:
        # 获取第几页
        page_num = request.GET.get('page')  # 添加默认值，防止没有参数导致的异常错误
        # 获取每页多少条
        page_size = request.GET.get('rows')  # 添加默认值，防止没有参数导致的异常错误

        # 接收参数
        name = request.GET.get('name', '')  # 没有值为None
        khno = request.GET.get('khno', '')
        state = request.GET.get('state', '')

        '''
            由于该功能可以带条件查询，所以key也必须多样化
            无条件查询
                customer:name_:khno_:state_
            有条件查询
                customer:name_zhangsan:khno_:state_
                customer:name_:khno_2018001:state_
                customer:name_:khno_:state_1
                customer:name_zhangsan:khno_2018001:state_1
        '''
        # 判断Redis中是否有缓存数据
        redis_key = 'customer:name_' + name + ':khno_' + khno + ':state_' + state
        redis_value = cache.get(redis_key)

        object_list = None
        if redis_value and len(redis_value) > 0:
            object_list = redis_value
        else:
            # 查询
            object_list = Customer.objects.values().all().order_by('-id')

            # 如果有条件则过滤查询
            if name:
                object_list = object_list.filter(name__icontains=name)

            if khno:
                object_list = object_list.filter(khno__icontains=khno)

            if state:
                object_list = object_list.filter(state=state)

            # 查询出结果放入redis缓存
            cache.set(redis_key, object_list, 3600)

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
    except Customer.DoesNotExist as e:
        pass


@require_POST
def create_customer(request):
    """添加用户信息"""
    try:
        # 接收参数
        data = request.POST.dict()
        # 弹出csrftoken
        data.pop('csrfmiddlewaretoken')
        # 生成客户编号
        result = ''
        for i in range(0, 3):
            result += str(randint(0, 9))

        khno = 'KH' + datetime.now().strftime('%Y%m%d%H%M%S') + result
        # 添加信息
        data['khno'] = khno
        Customer.objects.create(**data)

        # 清除缓存信息
        redis_keys = cache.keys('customer*')  # 模糊匹配所有kye，返回列表
        for k in redis_keys:
            cache.delete(k)

        # return JsonResponse({'code': 200, 'msg': '添加成功'})
        return JsonResponse(Message(msg='添加成功').result())
    except Exception as e:
        pass


@require_GET
def select_customer_by_id(request):
    """根据主键查询客户信息"""
    try:
        # 接收参数
        id = request.GET.get('id')
        # 查询
        c = Customer.objects.values().filter(pk=id)
        # 返回数据
        return JsonResponse(Message(obj=list(c)).result())
    except Customer.DoesNotExist as e:
        return JsonResponse(Message(code=400, msg='error').result())


@require_POST
def update_customer(request):
    """修改客户信息"""
    try:
        # 接收参数
        data = request.POST.dict()
        # 弹出csrftoken
        data.pop('csrfmiddlewaretoken')
        # 弹出主键
        id = data.pop('id')
        # 修改信息
        data['updateDate'] = datetime.now()
        Customer.objects.filter(pk=id).update(**data)

        # 清除缓存信息
        redis_keys = cache.keys('customer*')  # 模糊匹配所有kye，返回列表
        for k in redis_keys:
            cache.delete(k)

        # return JsonResponse({'code': 200, 'msg': '添加成功'})
        return JsonResponse(Message(msg='修改成功').result())
    except Exception as e:
        pass


@require_GET
def delete_customer(request):
    """删除客户信息"""
    try:
        # 接收参数
        ids = request.GET.get('ids')
        # 分割字符串
        ids = ids.split(',')
        # 删除
        cs = Customer.objects.filter(pk__in=ids).update(isValid=0, updateDate=datetime.now())

        # 清除缓存信息
        redis_keys = cache.keys('customer*')  # 模糊匹配所有kye，返回列表
        for k in redis_keys:
            cache.delete(k)

        return JsonResponse(Message(msg='删除成功').result())
    except Exception as e:
        pass


# -----------------------------------客户信息管理--------------------end--------------------

# -----------------------------------客户联系人管理-------------------start-------------------
@require_GET
def linkman_index(request):
    """跳转联系人首页"""
    # 接收参数
    id = request.GET.get('id')
    # 查询客户信息
    c = Customer.objects.get(pk=id)
    return render(request, 'customer/linkman.html', {'c': c})


@csrf_exempt
@require_POST
def select_linkman_by_customer_id(request, c_id):
    """根据客户主键查询联系人信息"""
    try:
        # 获取第几页
        page_num = request.POST.get('page', 1)  # 添加默认值，防止没有参数导致的异常错误

        # 获取每页多少条
        page_size = request.POST.get('rows', 10)  # 添加默认值，防止没有参数导致的异常错误

        # 查询
        c = Customer.objects.get(pk=c_id)
        object_list = LinkMan.objects.values().filter(customer=c).order_by('-id')

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
    except LinkMan.DoesNotExist as e:
        pass


@csrf_exempt
@require_POST
def create_linkman(request, c_id):
    """添加客户联系人"""
    # 接收参数
    data = request.POST.dict()
    # 弹出isNewRecord
    data.pop('isNewRecord')
    # 插入数据
    c = Customer.objects.get(pk=c_id)
    data['customer'] = c
    LinkMan.objects.create(**data)
    return JsonResponse(Message(msg='添加成功').result())


@csrf_exempt
@require_POST
def update_linkman(request):
    """修改客户联系人"""
    # 接收参数
    data = request.POST.dict()
    # 弹出主键
    id = data.pop('id')
    # 修改参数
    data['updateDate'] = datetime.now()
    LinkMan.objects.filter(pk=id).update(**data)
    return JsonResponse(Message(msg='修改成功').result())


@csrf_exempt
@require_POST
def delete_linkman(request):
    """删除客户开发计划"""
    # 接收参数
    data = request.POST.dict()
    # 弹出主键
    id = data.pop('id')
    # 逻辑删除
    LinkMan.objects.filter(pk=id).update(isValid=0, updateDate=datetime.now())
    return JsonResponse(Message(msg='删除成功').result())


# -----------------------------------客户联系人管理--------------------end--------------------

# -----------------------------------客户交往记录管理-------------------start-------------------
@require_GET
def contact_index(request):
    """跳转客户交往记录首页"""
    # 接收参数
    id = request.GET.get('id')
    # 查询客户信息
    c = Customer.objects.get(pk=id)
    return render(request, 'customer/contact.html', {'c': c})


@csrf_exempt
@require_POST
def select_contact_by_customer_id(request, c_id):
    """根据客户主键查询客户交往记录信息"""
    try:
        # 获取第几页
        page_num = request.POST.get('page', 1)  # 添加默认值，防止没有参数导致的异常错误

        # 获取每页多少条
        page_size = request.POST.get('rows', 10)  # 添加默认值，防止没有参数导致的异常错误

        # 查询
        c = Customer.objects.get(pk=c_id)
        object_list = Contact.objects.values().filter(customer=c).order_by('-id')

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
    except LinkMan.DoesNotExist as e:
        pass


@csrf_exempt
@require_POST
def create_contact(request, c_id):
    """添加客户交往记录"""
    # 接收参数
    data = request.POST.dict()
    # 弹出isNewRecord
    data.pop('isNewRecord')
    # 插入数据
    c = Customer.objects.get(pk=c_id)
    data['customer'] = c
    Contact.objects.create(**data)
    return JsonResponse(Message(msg='添加成功').result())


@csrf_exempt
@require_POST
def update_contact(request):
    """修改客户交往记录"""
    # 接收参数
    data = request.POST.dict()
    # 弹出主键
    id = data.pop('id')
    # 修改参数
    data['updateDate'] = datetime.now()
    Contact.objects.filter(pk=id).update(**data)
    return JsonResponse(Message(msg='修改成功').result())


@csrf_exempt
@require_POST
def delete_contact(request):
    """删除客户交往记录"""
    # 接收参数
    data = request.POST.dict()
    # 弹出主键
    id = data.pop('id')
    # 逻辑删除
    Contact.objects.filter(pk=id).update(isValid=0, updateDate=datetime.now())
    return JsonResponse(Message(msg='删除成功').result())


# -----------------------------------客户交往记录管理--------------------end--------------------


# -----------------------------------客户历史订单管理-------------------start-------------------
@require_GET
def order_index(request):
    """跳转客户历史订单首页"""
    # 接收参数
    id = request.GET.get('id')
    # 查询客户信息
    c = Customer.objects.get(pk=id)
    return render(request, 'customer/order.html', {'c': c})


@csrf_exempt
@require_POST
def select_order_by_customer_id(request, c_id):
    """根据客户主键查询客户历史订单信息"""
    try:
        # 获取第几页
        page_num = request.POST.get('page', 1)  # 添加默认值，防止没有参数导致的异常错误

        # 获取每页多少条
        page_size = request.POST.get('rows', 10)  # 添加默认值，防止没有参数导致的异常错误

        # 查询
        c = Customer.objects.get(pk=c_id)
        object_list = CustomerOrders.objects.values().filter(customer=c).order_by('-id')

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
    except LinkMan.DoesNotExist as e:
        pass


@require_GET
def select_order_by_id(request):
    """根据订单主键查询订单"""
    try:
        # 接收参数
        order_id = request.GET.get('order_id')

        # 查询
        co = CustomerOrders.objects.values().filter(pk=order_id)

        # 返回信息
        return JsonResponse(Message(obj=list(co)).result())
    except CustomerOrders.DoesNotExist as e:
        pass


@csrf_exempt
@require_POST
def select_order_detail_by_order_id(request, order_id):
    """根据订单主键查询订单详情"""
    try:
        # 获取第几页
        page_num = request.POST.get('page', 1)  # 添加默认值，防止没有参数导致的异常错误

        # 获取每页多少条
        page_size = request.POST.get('rows', 10)  # 添加默认值，防止没有参数导致的异常错误

        # 查询
        # co = CustomerOrders.objects.get(pk=order_id)
        object_list = OrdersDetail.objects.values().filter(order=order_id)

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
    except OrdersDetail.DoesNotExist as e:
        pass


# -----------------------------------客户历史订单管理--------------------end--------------------


# -----------------------------------客户流失管理-------------------start-------------------
@require_GET
def loss_index(request):
    """客户流失首页"""
    return render(request, 'customer/loss.html')


@require_GET
def select_loss(request):
    """查询客户流失信息"""
    try:
        # 获取第几页
        page_num = request.GET.get('page', 1)  # 添加默认值，防止没有参数导致的异常错误

        # 获取每页多少条
        page_size = request.GET.get('rows', 10)  # 添加默认值，防止没有参数导致的异常错误

        # 查询
        object_list = CustomerLoss.objects.values().all().order_by('-id')

        # 接收参数
        cusName = request.GET.get('cusName')
        if cusName:
            object_list = object_list.filter(cusName__icontains=cusName)

        cusManager = request.GET.get('cusManager')
        if cusManager:
            object_list = object_list.filter(cusManager__icontains=cusManager)

        state = request.GET.get('state')
        if state:
            object_list = object_list.filter(state=state)

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
    except OrdersDetail.DoesNotExist as e:
        pass


@require_GET
def reprieve_index(request):
    """根据主键查询客户流失信息"""
    try:
        # 接收参数
        id = request.GET.get('id')

        # 查询
        cl = CustomerLoss.objects.get(pk=id)

        # 返回数据
        return render(request, 'customer/reprieve.html', {'cl': cl})
    except CustomerLoss.DoesNotExist as e:
        pass


@csrf_exempt
@require_POST
def select_reprieve_by_loss_id(request, loss_id):
    """根据客户流失主键查询客户流失信息"""
    try:
        # 获取第几页
        page_num = request.POST.get('page', 1)  # 添加默认值，防止没有参数导致的异常错误

        # 获取每页多少条
        page_size = request.POST.get('rows', 10)  # 添加默认值，防止没有参数导致的异常错误

        # 查询
        cl = CustomerLoss.objects.get(pk=loss_id)
        object_list = CustomerReprieve.objects.values().filter(customerLoss=cl).order_by('-id')

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
    except LinkMan.DoesNotExist as e:
        pass


@csrf_exempt
@require_POST
def create_reprieve(request, loss_id):
    """添加客户流失信息"""
    # 接收参数
    data = request.POST.dict()
    # 弹出isNewRecord
    data.pop('isNewRecord')
    # 插入数据
    cl = CustomerLoss.objects.get(pk=loss_id)
    data['customerLoss'] = cl
    CustomerReprieve.objects.create(**data)
    return JsonResponse(Message(msg='添加成功').result())


@csrf_exempt
@require_POST
def update_reprieve(request):
    """修改客户流失信息"""
    # 接收参数
    data = request.POST.dict()
    # 弹出主键
    id = data.pop('id')
    # 修改参数
    data['updateDate'] = datetime.now()
    CustomerReprieve.objects.filter(pk=id).update(**data)
    return JsonResponse(Message(msg='修改成功').result())


@csrf_exempt
@require_POST
def delete_reprieve(request):
    """删除客户开发计划"""
    # 接收参数
    data = request.POST.dict()
    # 弹出主键
    id = data.pop('id')
    # 逻辑删除
    CustomerReprieve.objects.filter(pk=id).update(isValid=0, updateDate=datetime.now())
    return JsonResponse(Message(msg='删除成功').result())


@csrf_exempt
@require_POST
def ok_reprieve(request):
    """确认流失"""
    try:
        # 修改客户流失表，添加流失信息，修改state状态为1
        # 接收参数
        loss_id = request.POST.get('loss_id')
        lossReason = request.POST.get('lossReason')
        # 查询
        CustomerLoss.objects.filter(pk=loss_id) \
            .update(lossReason=lossReason, state=1, confirmLossTime=datetime.now(), updateDate=datetime.now())
        # 返回数据
        return JsonResponse(Message(msg='操作成功').result())
    except CustomerLoss.DoesNotExist as e:
        return JsonResponse(Message(code=400, msg='操作失败').result())


# -----------------------------------客户流失管理--------------------end--------------------


def select_customer_name(request):
    """查询客户名称"""
    try:
        # 查询
        d = Customer.objects.values('name').all()
        # 返回数据
        return JsonResponse(list(d), safe=False)
    except Exception as e:
        return JsonResponse({'code': 400, 'msg': 'error'})
