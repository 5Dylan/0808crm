from django.shortcuts import render
import pymysql

from crm.common import permission_required
from dbutil import pymysql_pool
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from sales.models import SaleChance, CusDevPlan
from datetime import datetime
from customer.models import LinkMan

# 准备数据
config = {
    'host': 'localhost',  # 数据库ip
    'port': 3306,  # 数据库用户名
    'user': 'root',  # 数据库密码
    'password': 'root',  # 数据库端口
    'database': 'db_crm',  # 具体的一个库 等价于database
    'charset': 'utf8mb4',  # 字符集
    # 默认获取的数据是元祖类型，如果想要或者字典类型的数据
    'cursorclass': pymysql.cursors.DictCursor
}

# 初始化连接池对象
connect_pool = pymysql_pool.ConnectionPool(size=50, name='mysql_pool', **config)


# 从连接池中获取连接
def connect():
    # 从连接池中获取连接
    connection = connect_pool.get_connection()
    return connection


# ----------------------------------------营销机会----------------------start------------------------
def sale_chance_index(request):
    """跳转营销机会首页"""
    return render(request, 'sales/sale_chacne.html')


@csrf_exempt
@require_POST
def select_sale_chacne_list(request):
    """查询所有营销机会"""
    try:
        # 获取第几页
        page_num = request.POST.get('page')
        # 获取每页多少条
        page_size = request.POST.get('rows')

        # 获取连接
        connection = connect()
        # 创建游标对象
        cursor = connection.cursor()

        # 编写sql
        sql = '''
            SELECT
                sc.id id, # 主键
                c.id customerId,  # 客户表主键
                c.khno khno,  # 客户编号
                c.name customerName,  # 客户名称
                sc.overview overview,  # 概要
                sc.create_man createMan,  # 创建人
                cl.id linkManId,  # 联系人主键
                cl.link_name linkManName,  # 联系人姓名
                cl.phone linkPhone,  # 联系电话
                u.user_name assignMan,  # 指派人名称
                sc.assign_time assignTime,  # 指派时间
                sc.state state,  # 分配状态
                sc.dev_result devResult  # 开发状态
            FROM
                t_sale_chance sc
            LEFT JOIN t_customer c ON sc.customer_id = c.id
            LEFT JOIN t_customer_linkman cl ON sc.link_man = cl.id
            LEFT JOIN t_user u ON sc.assign_man = u.id
            WHERE 1=1 AND sc.is_valid = 1 
        '''

        # 如果用户选择了其他条件，拼接sql
        # 客户名称
        customerName = request.POST.get('customerName')
        # 概要
        overview = request.POST.get('overview')
        # 创建人
        createMan = request.POST.get('createMan')
        # 分配状态
        state = request.POST.get('state')

        if customerName:
            sql += ' AND c.name like "%{}%" '.format(customerName)

        if overview:
            sql += ' AND sc.overview like "%{}%" '.format(overview)

        if createMan:
            sql += ' AND sc.create_man like "%{}%" '.format(createMan)

        if state:
            sql += ' AND sc.state = {} '.format(state)

        sql += ' ORDER BY sc.id DESC;'

        # 执行sql
        cursor.execute(sql)

        # 返回多条结果行
        object_list = cursor.fetchall()  # 查询当前sql执行后所有的记录

        # 关闭游标
        cursor.close()

        # 初始化分页对象
        p = Paginator(object_list, page_size)

        # 获取指定页数的数据
        data = p.page(page_num).object_list

        # 返回总条数
        count = p.count

        # 返回数据
        context = {
            'total': count,
            'rows': data
        }
        return JsonResponse(context)
    except Exception as e:
        print(e)
        return JsonResponse({'code': 400, 'msg': 'error'})
    finally:
        # 关闭连接
        connection.close()


# 添加营销机会 和 联系人
# 添加营销机会的权限值是101001
@require_POST
@permission_required('101001')
def create_sale_chance(request):
    try:
        '''
        # 从session中获取用户的权限值
        user_permission = request.session.get('user_permission')
        if not user_permission or '101001' not in user_permission:
            return JsonResponse({'code': 400, 'msg': '没有操作权限，请联系系统管理员'})
        '''

        # 接收参数
        customerId = request.POST.get('customerId').strip()
        customerName = request.POST.get('customerName_hidden').strip()
        chanceSource = request.POST.get('chanceSource').strip()
        linkMan = request.POST.get('linkMan').strip()
        linkManName = request.POST.get('linkManName').strip()
        linkPhone = request.POST.get('linkPhone').strip()
        cgjl = request.POST.get('cgjl').strip()
        overview = request.POST.get('overview').strip()
        description = request.POST.get('description').strip()
        username = request.POST.get('username').strip()

        # 如果有联系人还要添加联系人表数据
        if linkMan:
            lm = LinkMan(cusId=customerId, linkName=linkManName, phone=linkPhone)
            lm.save()

        # 默认参数 -> 开发状态 创建人 分配状态
        # 如果有分配人，添加分配时间，分配状态为已分配
        if username is not '0':
            sc = SaleChance(customerId=customerId, customerName=customerName,
                            chanceSource=chanceSource, linkMan=linkMan, linkPhone=linkPhone,
                            cgjl=cgjl, overview=overview, description=description,
                            assignMan=username, assignTime=datetime.now(), state=1, devResult=0,
                            createMan=request.session.get('username_session'))
        else:
            sc = SaleChance(customerId=customerId, customerName=customerName,
                            chanceSource=chanceSource, linkMan=linkMan, linkPhone=linkPhone,
                            cgjl=cgjl, overview=overview, description=description, devResult=0,
                            state=0, createMan=request.session.get('username_session'))

        # 插入数据
        sc.save()

        # 返回提示信息
        return JsonResponse({'code': 200, 'msg': '添加成功'})
    except Exception as e:
        print(e)
        return JsonResponse({'code': 400, 'msg': '添加失败'})


@require_GET
def select_sale_chance_by_id(request):
    """根据主键查询营销机会"""
    try:
        # 接收参数
        id = request.GET.get('id')

        # 获取连接
        connection = connect()
        # 创建游标对象
        cursor = connection.cursor()

        # 编写sql
        sql = '''
               SELECT
                   sc.id id, # 主键
                   c.id customerId,  # 客户表主键
                   c.khno khno,  # 客户编号
                   c.name customerName,  # 客户名称
                   sc.overview overview,  # 概要
                   sc.create_man createMan,  # 创建人
                   cl.id linkManId,  # 联系人主键
                   cl.link_name linkManName,  # 联系人姓名
                   cl.phone linkPhone,  # 联系电话
                   u.user_name assignMan,  # 指派人名称
                   sc.assign_time assignTime,  # 指派时间
                   sc.state state,  # 分配状态
                   sc.dev_result devResult,  # 开发状态
                   u.id userId,  # 用户表主键
                   sc.chance_source chanceSource,  # 机会来源
                   sc.cgjl cgjl,  # 成功几率
                   sc.description description  # 机会描述
               FROM
                   t_sale_chance sc
               LEFT JOIN t_customer c ON sc.customer_id = c.id
               LEFT JOIN t_customer_linkman cl ON sc.link_man = cl.id
               LEFT JOIN t_user u ON sc.assign_man = u.id
               WHERE 1=1 AND sc.id = %s
               '''

        # 执行sql
        cursor.execute(sql, (id,))

        # 返回结果
        object = cursor.fetchone()

        # 关闭游标
        cursor.close()

        return JsonResponse({'code': 200, 'msg': 'success', 'sc': object})
    except SaleChance.DoesNotExist as e:
        pass
    finally:
        connection.close()


@csrf_exempt
@require_POST
def update_sale_chance(request):
    """修改营销机会"""
    try:
        # 接收参数
        data = request.POST.dict()
        # 弹出主键
        id = data.pop('id')
        # 如果没有分配人，则修改状态为未分配
        assignMan = data.get('assignMan')
        if '0' == assignMan:
            data['state'] = 0
        else:
            data['state'] = 1
        # 修改数据
        SaleChance.objects.filter(pk=id).update(**data)
        # 返回提示信息
        return JsonResponse({'code': 200, 'msg': '修改成功'})
    except Exception as e:
        return JsonResponse({'code': 400, 'msg': '修改失败'})


@csrf_exempt
@require_POST
def delete_sale_chance(request):
    """逻辑删除客户信息"""
    try:
        # 接收参数
        ids = request.POST.get('ids')

        # 获取连接
        connection = connect()
        # 创建游标对象
        cursor = connection.cursor()

        # 编写sql
        # 循环操作
        ids = ids.split(',')
        for id in ids:
            sql = 'UPDATE t_sale_chance SET is_valid = 0 WHERE id = %s;'
            # 执行sql
            cursor.execute(sql, (id,))

        # 提交
        connection.commit()

        # 关闭游标
        cursor.close()

        # 返回信息
        return JsonResponse({'code': 200, 'msg': '删除成功'})
    except Exception as e:
        return JsonResponse({'code': 400, 'msg': '删除失败'})
    finally:
        # 关闭连接
        connection.close()


# ----------------------------------------营销机会-----------------------end-------------------------

# ----------------------------------------客户开发计划-----------------------start-------------------------
def cus_dev_plan_index(request):
    """跳转客户开发计划首页"""
    return render(request, 'sales/cus_dev_plan.html')


@csrf_exempt
@require_POST
def select_sale_chacne_for_cus_dev_plan(request):
    """查询所有营销机会"""
    try:
        # 获取第几页
        page_num = request.POST.get('page')
        # 获取每页多少条
        page_size = request.POST.get('rows')

        # 获取连接
        connection = connect()
        # 创建游标对象
        cursor = connection.cursor()

        # 编写sql
        sql = '''
            SELECT
                sc.id id, # 主键
                c.id customerId,  # 客户表主键
                c.khno khno,  # 客户编号
                c.name customerName,  # 客户名称
                sc.overview overview,  # 概要
                sc.create_man createMan,  # 创建人
                cl.id linkManId,  # 联系人主键
                cl.link_name linkManName,  # 联系人姓名
                cl.phone linkPhone,  # 联系电话
                u.user_name assignMan,  # 指派人名称
                sc.assign_time assignTime,  # 指派时间
                sc.state state,  # 分配状态
                sc.dev_result devResult  # 开发状态
            FROM
                t_sale_chance sc
            LEFT JOIN t_customer c ON sc.customer_id = c.id
            LEFT JOIN t_customer_linkman cl ON sc.link_man = cl.id
            LEFT JOIN t_user u ON sc.assign_man = u.id
            WHERE 1=1 AND sc.is_valid = 1 AND sc.state = 1 
        '''

        # 如果用户选择了其他条件，拼接sql
        # 客户名称
        customerName = request.POST.get('customerName')
        # 概要
        overview = request.POST.get('overview')
        # 开发状态
        devResult = request.POST.get('devResult')

        if customerName:
            sql += ' AND c.name like "%{}%" '.format(customerName)

        if overview:
            sql += ' AND sc.overview like "%{}%" '.format(overview)

        if devResult:
            sql += ' AND sc.dev_result = {} '.format(devResult)

        sql += ' ORDER BY sc.id DESC;'

        # 执行sql
        cursor.execute(sql)

        # 返回多条结果行
        object_list = cursor.fetchall()  # 查询当前sql执行后所有的记录

        # 关闭游标
        cursor.close()

        # 初始化分页对象
        p = Paginator(object_list, page_size)

        # 获取指定页数的数据
        data = p.page(page_num).object_list

        # 返回总条数
        count = p.count

        # 返回数据
        context = {
            'total': count,
            'rows': data
        }
        return JsonResponse(context)
    except Exception as e:
        print(e)
        return JsonResponse({'code': 400, 'msg': 'error'})
    finally:
        # 关闭连接
        connection.close()


@require_GET
def select_sale_chance_by_id_for_page(request, sale_chance_id):
    """根据主键查询营销机会跳转详细页"""
    try:
        # 接收参数 判断是开发客户还是查看详情
        flag = request.GET.get('flag')

        # 获取连接
        connection = connect()
        # 创建游标对象
        cursor = connection.cursor()

        # 编写sql
        sql = '''
            SELECT
                    sc.id id, # 主键
                    c.name customerName,  # 客户名称
                    sc.chance_source chanceSource,  # 机会来源
                    cl.link_name linkManName,  # 联系人姓名
                    cl.phone linkPhone,  # 联系电话
                    sc.cgjl cgjl,  # 成功几率
                    sc.overview overview,  # 概要
                    sc.description description,  # 机会描述
                    sc.create_man createMan,  # 创建人
                    sc.create_date createDate,  # 创建时间
                    u.user_name assignMan,  # 指派人名称
                    sc.assign_time assignTime  # 指派时间
            FROM
                    t_sale_chance sc
            LEFT JOIN t_customer c ON sc.customer_id = c.id
            LEFT JOIN t_customer_linkman cl ON sc.link_man = cl.id
            LEFT JOIN t_user u ON sc.assign_man = u.id
            WHERE 1=1 AND sc.id = %s;
        '''

        # 执行sql
        cursor.execute(sql, (sale_chance_id,))

        # 返回结果
        sc = cursor.fetchone()

        # 关闭游标
        cursor.close()

        # 返回数据
        return render(request, 'sales/cus_dev_plan_detail.html', {'sc': sc, 'flag': flag})
    except SaleChance.DoesNotExist as e:
        pass
    finally:
        connection.close()


@csrf_exempt
@require_POST
def select_cus_dev_plan_by_sale_chance_id(request, sale_chance_id):
    """根据营销机会主键查询所有开发计划"""
    try:
        # 获取第几页
        page_num = request.POST.get('page', 1)  # 添加默认值，防止没有参数导致的异常错误

        # 获取每页多少条
        page_size = request.POST.get('rows', 10)  # 添加默认值，防止没有参数导致的异常错误

        # 查询
        object_list = CusDevPlan.objects.values().filter(saleChance=sale_chance_id).order_by('-id')

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
    except CusDevPlan.DoesNotExist as e:
        pass


@csrf_exempt
@require_POST
def create_cus_dev_plan(request, sale_chance_id):
    """添加客户开发计划"""
    # 接收参数
    data = request.POST.dict()
    # 弹出isNewRecord
    data.pop('isNewRecord')
    # 插入数据
    sc = SaleChance.objects.get(pk=sale_chance_id)
    data['saleChance'] = sc
    CusDevPlan.objects.create(**data)
    # 修改营销机会表的开发状态为开发中
    SaleChance.objects.filter(pk=sale_chance_id).update(devResult=1)
    return JsonResponse({'code': 200, 'msg': '添加成功'})


@csrf_exempt
@require_POST
def update_cus_dev_plan(request):
    """修改客户开发计划"""
    # 接收参数
    data = request.POST.dict()
    # 弹出主键
    id = data.pop('id')
    # 修改参数
    data['updateDate'] = datetime.now()
    CusDevPlan.objects.filter(pk=id).update(**data)
    return JsonResponse({'code': 200, 'msg': '添加成功'})


@csrf_exempt
@require_POST
def delete_cus_dev_plan(request):
    """删除客户开发计划"""
    # 接收参数
    data = request.POST.dict()
    # 弹出主键
    id = data.pop('id')
    # 逻辑删除
    CusDevPlan.objects.filter(pk=id).update(isValid=0, updateDate=datetime.now())
    return JsonResponse({'code': 200, 'msg': '添加成功'})


def update_dev_result(request):
    """修改开发状态"""
    # 接收参数
    dev_result = request.GET.get('dev_result')
    sale_chance_id = request.GET.get('sale_chance_id')

    # 修改
    SaleChance.objects.filter(pk=sale_chance_id).update(devResult=dev_result)
    return JsonResponse({'code': 200, 'msg': '操作成功'})
# ----------------------------------------客户开发计划------------------------end--------------------------
