from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.http import require_POST, require_GET
from .models import User, UserRole, Role, Permission, Module
from django.http import JsonResponse
from email.header import Header  # 如果包含中文，需要通过Header对象进行编码
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib  # 负责发送邮件
import uuid
from datetime import datetime, timedelta
from hashlib import md5
import base64
from django.views.decorators.csrf import csrf_exempt
from crm.common import Message, is_empty


# 跳转登录和注册页面
def login_register(request):
    return render(request, 'system/login_register.html')


# 验证用户名是否唯一
@require_POST
def unique_username(request):
    try:
        # 接收参数
        username = request.POST.get('username')

        # 查询是否有该用户
        user = User.objects.get(username=username)

        # 有用户返回页面json
        return JsonResponse({'code': 400, 'msg': '用户名已存在'})
    except User.DoesNotExist as e:
        # 异常信息说明用户不存在
        return JsonResponse({'code': 200, 'msg': '恭喜你，可以注册'})


# 验证邮箱是否唯一
@require_POST
def unique_email(request):
    try:
        # 接收参数
        email = request.POST.get('email')

        # 查询是否有该用户
        user = User.objects.get(email=email)

        # 有用户返回页面json
        return JsonResponse({'code': 400, 'msg': '邮箱已存在'})
    except User.DoesNotExist as e:
        # 异常信息说明用户不存在
        return JsonResponse({'code': 200, 'msg': '恭喜你，可以注册'})


# -----------------email模块构建邮件发送实体对象--------------
# 格式化邮箱(不格式化会被当做垃圾邮件去发送或者发送失败)
def format_addr(s):
    name, addr = parseaddr(s)  # 比如：尚学堂 <java_mail01@163.com>
    # 因为name可能会有中文，需要对中文进行编码
    return formataddr((Header(name, 'utf-8').encode('utf-8'), addr))


# 邮件发送
@require_POST
def send_email(request):
    try:
        # --------------------------准备数据-------------start-------------
        # 发送邮箱
        from_addr = "java_mail01@163.com"
        # 程序代码中登录的密码其实就是那个你设置的授权码
        password = "sxt0523"
        # 发送服务器
        smtp_server = "smtp.163.com"
        # 接收邮箱
        to_addr = request.POST.get('email')

        # 用户名
        username = request.POST.get('username')
        # 密码
        u_pwd = request.POST.get('password')
        # 使用md5加密
        u_pwd = md5(u_pwd.encode(encoding='utf-8')).hexdigest()
        # 激活码
        code = ''.join(str(uuid.uuid4()).split('-'))
        # 10分钟后的时间戳
        td = timedelta(minutes=10)
        ts = datetime.now() + td
        ts = str(ts.timestamp()).split('.')[0]
        # --------------------------准备数据---------------end-----------

        # -----------------------插入数据库数据----------start--------------
        user = User(username=username, password=u_pwd, email=to_addr, code=code, timestamp=ts)
        user.save()
        # -----------------------插入数据库数据----------end--------------

        # ------------------------构建邮件内容对象----------start--------------
        html = """
                <html>
                    <body>
                        <div>
                        Email 地址验证<br>
                        这封信是由 上海尚学堂 发送的。<br>
                        您收到这封邮件，是由于在 上海尚学堂CRM系统 进行了新用户注册，或用户修改 Email 使用了这个邮箱地址。<br>
                        如果您并没有访问过 上海尚学堂CRM，或没有进行上述操作，请忽略这封邮件。您不需要退订或进行其他进一步的操作。<br>
                        ----------------------------------------------------------------------<br>
                         帐号激活说明<br>
                        ----------------------------------------------------------------------<br>
                        如果您是 上海尚学堂CRM 的新用户，或在修改您的注册 Email 时使用了本地址，我们需要对您的地址有效性进行验证以避免垃圾邮件或地址被滥用。<br>
                        您只需点击下面的链接激活帐号即可：<br>
                        <a href="http://www.crm.com/system/active_accounts/?username={}&code={}&timestamp={}">http://www.crm.com/system/active_accounts/?username={}&amp;code={}&amp;timestamp={}</a><br/>
                        感谢您的访问，祝您生活愉快！<br>
                        此致<br>
                         上海尚学堂 管理团队.
                        </div>
                    </body>
                </html>
             """.format(username, code, ts, username, code, ts)
        msg = MIMEText(html, "html", "utf-8")

        # 标准邮件需要三个头部信息： From To 和 Subject
        # 设置发件人和收件人的信息 u/U:表示unicode字符串
        # 比如：尚学堂 <java_mail01@163.com>
        msg['From'] = format_addr(u'尚学堂<%s>' % from_addr)  # 发件人
        to_name = username  # 收件人名称
        msg['To'] = format_addr(u'{}<%s>'.format(to_name) % to_addr)  # 收件人

        # 设置标题
        # 如果接收端的邮件列表需要显示发送者姓名和发送地址就需要设置Header，同时中文需要encode转码
        msg['Subject'] = Header(u'CRM系统官网帐号激活邮件', 'utf-8').encode()
        # ------------------------构建邮件内容对象-----------end-------------

        # ------------------------------发送--------------start----------------
        # 创建发送邮件服务器的对象
        server = smtplib.SMTP(smtp_server, 25)
        # 设置debug级别0就不打印发送日志，1打印
        server.set_debuglevel(1)
        # 登录发件邮箱
        server.login(from_addr, password)
        # 调用发送方法 第一个参数是发送者邮箱，第二个是接收邮箱，第三个是发送内容
        server.sendmail(from_addr, [to_addr], msg.as_string())
        # 关闭发送
        server.quit()
        # ------------------------------发送----------------end--------------

        # 返回页面提示信息
        return JsonResponse({'code': 200, 'msg': '注册成功，请前往邮箱激活帐号'})
    except smtplib.SMTPException as e:
        # 返回页面提示信息
        return JsonResponse({'code': 400, 'msg': '注册失败，请重新注册'})


# 激活帐号
@require_GET
def active_accounts(request):
    try:
        # 用户名
        username = request.GET.get('username')
        # 激活码
        code = request.GET.get('code')
        # 过期时间
        ts = request.GET.get('timestamp')

        # 根据用户名和激活码查询是否有该帐号
        user = User.objects.get(username=username, code=code, timestamp=ts)

        # 根据过期时间判断帐号是否有效
        now_ts = int(str(datetime.now().timestamp()).split('.')[0])
        if now_ts > int(ts):
            # 链接失效，返回提示信息，删除数据库信息
            user.delete()
            return HttpResponse(
                '<h1>该链接已失效，请重新注册&nbsp;&nbsp;<a href="http://www.crm.com/login_register/">上海尚学堂CRM系统</a></h1>')

        # 没有过期，激活帐号，清除激活码，改变状态
        user.code = ''  # 清除激活码
        user.status = 1  # 有效帐号
        user.save()

        # 返回提示信息
        return HttpResponse(
            '<h1>帐号激活成功，请前往系统登录&nbsp;&nbsp;<a href="http://www.crm.com/login_register/">上海尚学堂CRM系统</a></h1>')
    except Exception as e:
        if isinstance(e, User.DoesNotExist):
            return HttpResponse(
                '<h1>该链接已失效，请重新注册&nbsp;&nbsp;<a href="http://www.crm.com/login_register/">上海尚学堂CRM系统</a></h1>')
        return HttpResponse('<h1>不好意思，网络出现了波动，激活失败，请重新尝试</h1>')


# 登录
@require_POST
def login_user(request):
    try:
        # 删除该用户的所有session信息
        del request.session['username_session']
        del request.session['user_permission']
    except Exception as e:
        pass

    try:
        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        # 使用md5加密
        password_md5 = md5(password.encode(encoding='utf-8')).hexdigest()

        # 查询
        user = User.objects.get(username=username, password=password_md5)

        # 查询session中是否存在用户信息，没有则添加session
        username_session = request.session.get('username_session')
        if not username_session:
            # 如果用户存在，存储sesison信息
            request.session['username_session'] = username
            # 设置session失效时间，关闭浏览器session失效
            request.session.set_expiry(0)

        # 如果用户存在，查询用户所拥有的权限
        # 根据用户查询角色
        # role_id = UserRole.objects.values_list('role', flat=True).filter(user__id=user.id).all()
        role_id = user.roles.values_list('id', flat=True).all()
        # 根据角色查询模块
        module_id = Permission.objects.values_list('module', flat=True).filter(role__id__in=role_id)
        # 根据模块获取资源
        opt_value = list(Module.objects.values_list('optValue', flat=True).filter(pk__in=module_id))
        # 根据用户将资源信息添加至session
        request.session['user_permission'] = opt_value
        # 设置session失效时间，关闭浏览器session失效
        request.session.set_expiry(0)

        # 返回成功提示信息
        context = {
            'code': 200,
            'msg': '欢迎回来',
            'opt_value': opt_value
        }

        # 如果用户存在，前台js存储cookie
        # 存储格式：key -> login_cookie, value -> username&password

        # 由于功能改造，代码重构
        if 'true' == remember:
            context['login_username_cookie'] = base64.b64encode(username.encode(encoding='utf-8')).decode(
                encoding='utf-8')
            context['login_password_cookie'] = base64.b64encode(password.encode(encoding='utf-8')).decode(
                encoding='utf-8')

        return JsonResponse(context)
    except User.DoesNotExist as e:
        # 返回错误提示信息
        return JsonResponse({'code': 400, 'msg': '用户名或密码错误'})


# 跳转首页
def index(request):
    # 判断session中是否有用户信息
    username = request.session.get('username_session')

    if username:
        return render(request, 'system/index.html')

    # 如果不存在，重定向登录页面
    return redirect('system:login_register')


# 修改密码
@require_POST
def update_password(request):
    try:
        # 接收参数
        username = request.POST.get('username')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        # 使用md5加密
        old_password_md5 = md5(old_password.encode(encoding='utf-8')).hexdigest()

        # 查询用户密码是否正确
        user = User.objects.get(username=username, password=old_password_md5)

        # 使用md5加密
        new_password_md5 = md5(new_password.encode(encoding='utf-8')).hexdigest()

        # 修改密码
        user.password = new_password_md5
        user.save()

        # 修改密码要重新登录，所以要安全退出
        # 安全退出系统要清除session，所以这里不写

        # 返回页面信息
        return JsonResponse({'code': 200, 'msg': '修改成功'})
    except User.DoesNotExist as e:
        return JsonResponse({'code': 400, 'msg': '原密码输入错误'})


# 安全退出
def logout(request):
    try:
        # 清除session
        request.session.flush()

        # 重定向至登录页面
        return redirect('system:login_register')
    except Exception as e:
        # 重定向至登录页面
        return redirect('system:login_register')


def select_customer_manager(request):
    """查询客户经理"""
    u = User.objects.values('username').filter(roles__roleName='客户经理')
    # 返回数据
    return JsonResponse(list(u), safe=False)


# -----------------------------------系统管理------------start--------------------
@require_GET
def module_index(request):
    """模块管理首页"""
    return render(request, 'system/module.html')


@require_GET
def select_module(request):
    """查询所有模块信息"""
    try:
        # 获取第几页
        page_num = request.GET.get('page', 1)  # 添加默认值，防止没有参数导致的异常错误

        # 获取每页多少条
        page_size = request.GET.get('rows', 10)  # 添加默认值，防止没有参数导致的异常错误

        # 查询
        # {'模型属性名': 'select DATE_FORMAT(数据库列名, '格式化样式')'}
        select = {'createDate': "select DATE_FORMAT(create_date, '%%Y-%%m-%%d %%H:%%i:%%s')",
                  'updateDate': "select DATE_FORMAT(update_date, '%%Y-%%m-%%d %%H:%%i:%%s')"}

        # 如果使用后台格式化日期，必须将要格式化的列展示在values()参数中
        queryset = Module.objects.extra(select=select).values('id', 'moduleName', 'moduleStyle',
                                                              'url', 'optValue', 'grade', 'orders', 'parent',
                                                              'createDate', 'updateDate').order_by('orders').all()

        # 初始化分页对象
        p = Paginator(queryset, page_size)

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
    except Module.DoesNotExist as e:
        pass


@require_GET
def select_module_by_grade(request):
    """根据层级查询模块信息"""
    try:
        # 接收参数
        grade = request.GET.get('grade')

        m = Module.objects.values('id', 'moduleName').filter(grade=grade).all()

        return JsonResponse(list(m), safe=False)
    except Module.DoesNotExist as e:
        pass


@csrf_exempt
@require_POST
def create_module(request):
    """添加模块信息"""
    try:
        # 接收参数
        data = request.POST.dict()
        data.pop('id')

        # 如果权限值已存在，提示错误
        opt_value = data.get('optValue')
        Module.objects.get(optValue=opt_value)
        return JsonResponse(Message(code=400, msg='权限值已存在，请重新选择').result())
    except Module.DoesNotExist as e:
        pass

    # 如果有父级菜单查询父级对象插入
    parent = data.pop('parent')
    if parent:
        p = Module.objects.get(pk=parent)
        data['parent'] = p

    # 添加数据
    Module.objects.create(**data)
    return JsonResponse(Message(msg='添加成功').result())


@csrf_exempt
@require_POST
def update_module(request):
    """修改模块信息"""
    try:
        # 接收参数
        data = request.POST.dict()
        id = data.pop('id')

        # 如果权限值被修改，判断是否存在，已存在，提示错误
        opt_value = data.get('optValue')
        # 查询原来的模块信息
        m = Module.objects.get(pk=id)
        # 判断是否权限值被修改
        if opt_value != m.optValue:
            # 判断是否存在
            Module.objects.get(optValue=opt_value)
            return JsonResponse(Message(code=400, msg='权限值已存在，请重新选择').result())
    except Module.DoesNotExist as e:
        pass

    # 如果父级id存在并且父级id被修改
    parent = data.pop('parent')
    if parent and parent != str(m.parent_id):
        p = Module.objects.get(pk=parent)
        data['parent'] = p

    # 修改数据
    Module.objects.filter(pk=id).update(**data, updateDate=datetime.now())
    return JsonResponse(Message(msg='修改成功').result())


@require_GET
def delete_module(request):
    """删除模块信息"""
    # 接收参数
    ids = request.GET.get('ids')
    Module.objects.filter(pk__in=ids.split(',')).delete()
    return JsonResponse(Message(msg='删除成功').result())


@require_GET
def roel_index(request):
    """角色管理首页"""
    return render(request, 'system/role.html')


@require_GET
def select_role(request):
    """查询所有角色信息"""
    try:
        # 获取第几页
        page_num = request.GET.get('page', 1)  # 添加默认值，防止没有参数导致的异常错误

        # 获取每页多少条
        page_size = request.GET.get('rows', 10)  # 添加默认值，防止没有参数导致的异常错误

        # 查询
        # {'模型属性名': 'select DATE_FORMAT(数据库列名, '格式化样式')'}
        select = {'createDate': "select DATE_FORMAT(create_date, '%%Y-%%m-%%d %%H:%%i:%%s')",
                  'updateDate': "select DATE_FORMAT(update_date, '%%Y-%%m-%%d %%H:%%i:%%s')"}

        # 如果使用后台格式化日期，必须将要格式化的列展示在values()参数中
        queryset = Role.objects.extra(select=select).values('id', 'roleName', 'roleRemark',
                                                            'createDate', 'updateDate').order_by('-id').all()

        # 初始化分页对象
        p = Paginator(queryset, page_size)

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
    except Module.DoesNotExist as e:
        pass


@csrf_exempt
@require_POST
def create_role(request):
    """添加角色信息"""
    try:
        # 接收参数
        data = request.POST.dict()
        data.pop('id')

        # 如果角色已存在，提示错误
        roleName = data.get('roleName')
        Role.objects.get(roleName=roleName)
        return JsonResponse(Message(code=400, msg='角色名已存在，请重新添加').result())
    except Role.DoesNotExist as e:
        pass

    # 添加数据
    Role.objects.create(**data)
    return JsonResponse(Message(msg='添加成功').result())


@csrf_exempt
@require_POST
def update_role(request):
    """修改角色信息"""
    try:
        # 接收参数
        data = request.POST.dict()
        id = data.pop('id')

        # 如果角色被修改，判断是否存在，已存在，提示错误
        roleName = data.get('roleName')
        # 查询原来的角色信息
        r = Role.objects.get(pk=id)
        # 判断角色是否被修改
        if roleName != r.roleName:
            # 判断是否存在
            Role.objects.get(roleName=roleName)
            return JsonResponse(Message(code=400, msg='角色名已存在，请重新添加').result())
    except Role.DoesNotExist as e:
        pass

    # 修改数据
    data['updateDate'] = datetime.now()
    Role.objects.filter(pk=id).update(**data)
    return JsonResponse(Message(msg='添加成功').result())


@require_GET
def delete_role(request):
    """删除角色信息"""
    # 接收参数
    ids = request.GET.get('ids')
    Role.objects.filter(pk__in=ids.split(',')).update(isValid=0, updateDate=datetime.now())
    return JsonResponse(Message(msg='删除成功').result())


@require_GET
def role_module_index(request):
    """角色关联权限首页"""
    # 接收参数
    role_id = request.GET.get('id')
    # 查询角色
    role = Role.objects.get(pk=role_id)
    # 查询所有权限(模块)
    module = list(Module.objects.values('id', 'parent', 'moduleName').all())
    # 查询角色已拥有的权限(资源)
    role_module = Permission.objects.values_list('module', flat=True).filter(role__id=role_id).all()
    # 设置checked
    for m in module:
        if m.get('id') in role_module:
            m['checked'] = 'true'
        else:
            m['checked'] = 'false'

    # 返回数据
    context = {
        'role': role,
        'module': module
    }
    return render(request, 'system/role_module.html', context)


@csrf_exempt
@require_POST
def role_relate_module(request):
    """角色关联模块"""
    try:
        # 接收参数
        module_checked_id = request.POST.get('module_checked_id')
        role_id = request.POST.get('role_id')

        # 删除该角色拥有的所有权限
        Permission.objects.filter(role__id=role_id).delete()

        # 如果模块为空，则直接return
        if not module_checked_id:
            return JsonResponse(Message(msg='操作成功').result())

        # 查询角色和模块
        role = Role.objects.get(pk=role_id)
        module = Module.objects.filter(pk__in=module_checked_id.split(',')).all()

        # 循环插入数据
        for m in module:
            Permission.objects.create(role=role, module=m)

        return JsonResponse(Message(msg='操作成功').result())
    except Exception as e:
        return JsonResponse(Message(code=400, msg='操作失败').result())


@require_GET
def user_index(request):
    """用户管理首页"""
    return render(request, 'system/user.html')


@require_GET
def select_user(request):
    """查询所有用户信息"""
    try:
        # 获取第几页
        page_num = request.GET.get('page', 1)  # 添加默认值，防止没有参数导致的异常错误

        # 获取每页多少条
        page_size = request.GET.get('rows', 10)  # 添加默认值，防止没有参数导致的异常错误

        # 查询
        # {'模型属性名': 'select DATE_FORMAT(数据库列名, '格式化样式')'}
        select = {'create_date': "select DATE_FORMAT(create_date, '%%Y-%%m-%%d %%H:%%i:%%s')",
                  'update_date': "select DATE_FORMAT(update_date, '%%Y-%%m-%%d %%H:%%i:%%s')"}

        # 如果使用后台格式化日期，必须将要格式化的列展示在values()参数中
        queryset = User.objects.extra(select=select).values('id', 'username', 'truename',
                                                            'email', 'phone', 'create_date').order_by('-id').all()

        # 接收参数
        username = request.GET.get('username')
        if username:
            queryset = queryset.filter(username=username)

        # 初始化分页对象
        p = Paginator(queryset, page_size)

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
    except Module.DoesNotExist as e:
        pass


@require_GET
def select_role_for_user(request):
    """用户管理查询角色"""
    try:
        # 查询
        role = Role.objects.values('id', 'roleName').all().order_by('id')
        # 返回数据
        return JsonResponse(list(role), safe=False)
    except Role.DoesNotExist as e:
        pass


@csrf_exempt
@require_POST
def create_user(request):
    """添加用户信息"""
    try:
        # 接收参数
        data = request.POST.dict()
        data.pop('id')

        # 如果用户名已存在，提示错误
        username = data.get('username')
        User.objects.get(username=username)
        return JsonResponse(Message(code=400, msg='用户名已存在，请重新添加').result())
    except User.DoesNotExist as e:
        pass

    try:
        # 如果邮箱已存在，提示错误
        email = data.get('email')
        User.objects.get(email=email)
        return JsonResponse(Message(code=400, msg='邮箱已存在，请重新添加').result())
    except User.DoesNotExist as e:
        pass

    # 加密密码
    # 使用md5加密
    data['password'] = md5(data.get('password').encode(encoding='utf-8')).hexdigest()

    data.pop('roles')
    # role_ids = data.pop('roles_hidden')
    role_ids = request.POST.getlist('roles')

    # 添加数据
    user = User.objects.create(**data)

    # 插入用户角色中间表
    result = create_userrole(role_ids, user, is_create=True)

    '''
    # 插入用户角色中间表
    roles = Role.objects.filter(pk__in=role_ids).all()
    for role in roles:
        UserRole.objects.create(user=user, role=role)
    '''

    return JsonResponse(result)


@csrf_exempt
@require_POST
def update_user(request):
    """修改用户信息"""
    try:
        # 接收参数
        data = request.POST.dict()
        id = data.pop('id')

        user = User.objects.get(pk=id)

        username = data.get('username')
        # 如果用户名被更改，判断用户名是否存在
        if username and username != user.username:
            User.objects.get(username=username)
            return JsonResponse(Message(code=400, msg='用户名已存在，请重新添加').result())
    except User.DoesNotExist as e:
        pass

    try:
        # 如果邮箱被更改，判断邮箱是否存在
        email = data.get('email')
        if email and email != user.email:
            User.objects.get(email=email)
            return JsonResponse(Message(code=400, msg='邮箱已存在，请重新添加').result())
    except User.DoesNotExist as e:
        pass

    # 加密密码
    # 使用md5加密
    u_pwd = data.pop('password')
    if u_pwd:
        # 使用md5加密
        data['password'] = md5(u_pwd.encode(encoding='utf-8')).hexdigest()

    data.pop('roles')
    role_ids = request.POST.getlist('roles')

    '''
    # 删除所有该用户的角色
    UserRole.objects.filter(user__id=id).delete()

    # 修改用户角色中间表
    roles = Role.objects.filter(pk__in=role_ids).all()
    for role in roles:
        UserRole.objects.create(user=user, role=role)
    '''

    # 修改数据
    data['update_date'] = datetime.now()
    User.objects.filter(pk=id).update(**data)

    # 修改用户角色中间表
    result = create_userrole(role_ids, user)

    return JsonResponse(result)


def create_userrole(role_ids, user, is_create=False):
    """添加用户角色中间表"""
    if not is_create:
        # 删除所有该用户的角色
        # user.userrole_set.all().delete()
        UserRole.objects.filter(user__id=user.id).delete()

    roles = Role.objects.filter(pk__in=role_ids).all()
    for role in roles:
        UserRole.objects.create(user=user, role=role)

    return Message(msg='操作成功').result()


@require_GET
def select_role_by_userid(request):
    """根据用户id查询角色"""
    # 接收参数
    id = request.GET.get('id')
    role_ids = UserRole.objects.values_list('role', flat=True).filter(user__id=id).all()
    return JsonResponse(list(role_ids), safe=False)


@require_GET
def delete_user(request):
    """删除用户信息"""
    # 接收参数
    ids = request.GET.get('ids')
    # 逻辑删除
    User.objects.filter(pk__in=ids.split(',')).update(isValid=0, update_date=datetime.now())
    return JsonResponse(Message(msg='删除成功').result())

# -----------------------------------系统管理-------------end---------------------
