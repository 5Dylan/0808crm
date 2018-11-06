from django.db import models


class ModelManager(models.Manager):

    def get_queryset(self):
        return super(ModelManager, self).get_queryset().filter(isValid=1)


class Customer(models.Model):
    # 客户编号 KH + 日期 + 三位随指数
    khno = models.CharField(max_length=20, unique=True)
    # 客户名称
    name = models.CharField(max_length=20)
    # 客户所在地区
    area = models.CharField(max_length=20)
    # 客户经理
    cusManager = models.CharField(max_length=30, db_column='cus_manager')
    # 客户等级
    level = models.CharField(max_length=30)
    # 满意度
    myd = models.CharField(max_length=30)
    # 信用度
    xyd = models.CharField(max_length=30)
    # 地址
    address = models.CharField(max_length=100)
    # 邮编
    postCode = models.CharField(max_length=10, db_column='post_code')
    # 联系电话
    phone = models.CharField(max_length=18)
    # 传真
    fax = models.CharField(max_length=20)
    # 网址
    website = models.CharField(max_length=50, db_column='web_site')
    # 营业注册号
    yyzzzch = models.CharField(max_length=50)
    # 法人
    fr = models.CharField(max_length=20)
    # 注册资金
    zczj = models.CharField(max_length=20)
    # 年营业额
    nyye = models.CharField(max_length=20)
    # 开户银行
    khyh = models.CharField(max_length=20)
    # 开户账号
    khzh = models.CharField(max_length=20)
    # 地税
    dsdjh = models.CharField(max_length=20)
    # 国税
    gsdjh = models.CharField(max_length=20)
    # 状态0=正常 1=暂时流失 2=真正流失
    state = models.IntegerField(default=0)
    isValid = models.IntegerField(db_column='is_valid', default=1)
    createDate = models.DateTimeField(db_column='create_date', auto_now_add=True)
    updateDate = models.DateTimeField(db_column='update_date', auto_now_add=True)

    all = models.Manager()
    objects = ModelManager()

    class Meta:
        db_table = 't_customer'


# 客户联系人
class LinkMan(models.Model):
    # 客户id，外键
    # cusId = models.IntegerField(db_column='cus_id')
    customer = models.ForeignKey(Customer, db_column='cus_id', on_delete=models.DO_NOTHING)
    linkName = models.CharField(max_length=20, db_column='link_name')
    sex = models.CharField(max_length=4)
    zhiwei = models.CharField(max_length=20, db_column='zhiwei')
    officePhone = models.CharField(max_length=20, db_column='office_phone')
    phone = models.CharField(max_length=20, db_column='phone')

    isValid = models.IntegerField(db_column='is_valid', default=1)
    createDate = models.DateTimeField(db_column='create_date', auto_now_add=True)
    updateDate = models.DateTimeField(db_column='update_date', auto_now_add=True)

    objects = ModelManager()

    class Meta:
        db_table = 't_customer_linkman'


# 交往记录
class Contact(models.Model):
    customer = models.ForeignKey(Customer, db_column='cus_id', on_delete=models.DO_NOTHING)
    contactTime = models.DateTimeField(db_column='contact_time')
    address = models.CharField(max_length=120, db_column='address')
    overview = models.CharField(max_length=120, db_column='overview')
    isValid = models.IntegerField(db_column='is_valid', default=1)
    createDate = models.DateTimeField(db_column='create_date', auto_now_add=True)
    updateDate = models.DateTimeField(db_column='update_date', auto_now_add=True)

    objects = ModelManager()

    class Meta:
        db_table = 't_customer_contact'


# 客户订单
class CustomerOrders(models.Model):
    # 关联的客户
    customer = models.ForeignKey(Customer, db_column='cus_id', on_delete=models.DO_NOTHING)
    # 订单编号
    orderNo = models.DateTimeField(db_column='order_no')
    # 下单日期
    orderDate = models.DateTimeField(db_column='order_date', auto_now_add=True)
    # 收货地址
    address = models.CharField(max_length=120, db_column='address')
    # 订单总金额
    totalPrice = models.FloatField(db_column='total_price')
    # 0=未回款 1=已回款
    state = models.IntegerField()

    isValid = models.IntegerField(db_column='is_valid')
    createDate = models.DateTimeField(db_column='create_date', auto_now_add=True)
    updateDate = models.DateTimeField(db_column='update_date', auto_now_add=True)

    objects = ModelManager()

    class Meta:
        db_table = 't_customer_order'


# 订单详情表
class OrdersDetail(models.Model):
    # 关联订单
    order = models.ForeignKey(CustomerOrders, db_column='order_id', on_delete=models.DO_NOTHING)
    # 商品名称
    goodsName = models.CharField(max_length=100, db_column='goods_name')
    # 商品数量
    goodsNum = models.IntegerField(db_column='goods_num')
    # 单位
    unit = models.CharField(max_length=10, db_column='unit')
    # 单价
    price = models.FloatField(db_column='price')
    # 总价
    sum = models.FloatField(db_column='sum')

    isValid = models.IntegerField(db_column='is_valid')
    createDate = models.DateTimeField(db_column='create_date', auto_now_add=True)
    updateDate = models.DateTimeField(db_column='update_date', auto_now_add=True)

    objects = ModelManager()

    class Meta:
        db_table = 't_order_details'


# 客户流失表
class CustomerLoss(models.Model):
    # 客户编号
    cusNo = models.CharField(max_length=40, db_column='cus_no')
    # 客户名称
    cusName = models.CharField(max_length=20, db_column='cus_name')
    # 客户经理
    cusManager = models.CharField(max_length=20, db_column='cus_manager')
    # 上次下单日期
    lastOrderTime = models.DateTimeField(db_column='last_order_time', auto_now_add=True)
    # 确认流失日期
    confirmLossTime = models.DateTimeField(db_column='confirm_loss_time', auto_now_add=True)
    # 状态 0=暂缓流失 1=确认流失
    state = models.IntegerField()
    # 流失原因
    lossReason = models.CharField(max_length=1000, db_column='loss_reason')

    isValid = models.IntegerField(db_column='is_valid', default=1)
    createDate = models.DateTimeField(db_column='create_date', auto_now_add=True)
    updateDate = models.DateTimeField(db_column='update_date', auto_now_add=True)
    objects = ModelManager()

    class Meta:
        db_table = 't_customer_loss'


# 流失暂缓措施
class CustomerReprieve(models.Model):
    customerLoss = models.ForeignKey(CustomerLoss, db_column='loss_id', db_constraint=False,
                                     on_delete=models.DO_NOTHING)
    # 采取措施
    measure = models.CharField(max_length=1000, db_column='measure')

    isValid = models.IntegerField(db_column='is_valid', default=1)
    createDate = models.DateTimeField(db_column='create_date', auto_now_add=True)
    updateDate = models.DateTimeField(db_column='update_date', auto_now_add=True)

    objects = ModelManager()

    class Meta:
        db_table = 't_customer_reprieve'
