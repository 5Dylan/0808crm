from django.db import models


class ModelManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(isValid=1)


# 资源表
class Module(models.Model):
    # 资源名称
    moduleName = models.CharField(max_length=50, db_column='module_name')
    # 样式
    moduleStyle = models.CharField(max_length=120, db_column='module_style')
    # 跳转地址
    url = models.CharField(max_length=100, db_column='url')
    # 自关联
    parent = models.ForeignKey('self', db_column='parent_id', db_constraint=False, on_delete=models.DO_NOTHING)
    # 父级操作值
    parentOptValue = models.CharField(max_length=20, db_column='parent_opt_value')
    # 级别
    grade = models.IntegerField(db_column='grade')
    # 操作值
    optValue = models.CharField(max_length=20, db_column='opt_value')
    # 排序顺序
    orders = models.IntegerField(db_column='orders')
    isValid = models.IntegerField(db_column='is_valid', default=1)
    createDate = models.DateTimeField(db_column='create_date', auto_now_add=True)
    updateDate = models.DateTimeField(max_length=20, db_column='update_date', auto_now_add=True)

    objects = ModelManager()

    class Meta:
        db_table = 't_module'


# 角色表
class Role(models.Model):
    roleName = models.CharField(max_length=20, db_column='role_name')
    roleRemark = models.CharField(max_length=120, db_column='role_remark')
    isValid = models.IntegerField(db_column='is_valid', default=1)
    createDate = models.DateTimeField(db_column='create_date', auto_now_add=True)
    updateDate = models.DateTimeField(max_length=20, db_column='update_date', auto_now_add=True)

    permissions = models.ManyToManyField(Module, through="Permission", through_fields=('role', 'module'))

    objects = ModelManager()

    class Meta:
        db_table = 't_role'


# 角色-资源中间表
class Permission(models.Model):
    role = models.ForeignKey(Role, db_column='role_id', db_constraint=False, on_delete=models.DO_NOTHING)
    module = models.ForeignKey(Module, db_column='module_id', db_constraint=False, on_delete=models.DO_NOTHING)
    aclValue = models.CharField(max_length=20, db_column='acl_value')
    isValid = models.IntegerField(db_column='is_valid', default=1)
    createDate = models.DateTimeField(db_column='create_date', auto_now_add=True)
    updateDate = models.DateTimeField(max_length=20, db_column='update_date', auto_now_add=True)

    objects = ModelManager()

    class Meta:
        db_table = 't_permission'


# 用户模型
class User(models.Model):
    username = models.CharField(max_length=20, db_column='user_name')
    password = models.CharField(max_length=100)
    truename = models.CharField(max_length=20, null=True, db_column='true_name')
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=20, null=True)
    isValid = models.IntegerField(max_length=4, default=1, db_column='is_valid')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True)
    code = models.CharField(max_length=255, null=True)
    status = models.BooleanField(max_length=1, default=0)
    timestamp = models.CharField(max_length=255, null=True)

    roles = models.ManyToManyField(Role, through="UserRole", through_fields=('user', 'role'))

    objects = ModelManager()

    # 元信息
    class Meta(object):
        db_table = 't_user'


# 用户-角色中间表
class UserRole(models.Model):
    user = models.ForeignKey(User, db_column='user_id',
                             db_constraint=False, on_delete=models.DO_NOTHING)

    role = models.ForeignKey(Role, db_column='role_id',
                             db_constraint=False, on_delete=models.DO_NOTHING)

    isValid = models.IntegerField(db_column='is_valid', default=1)
    createDate = models.DateTimeField(db_column='create_date', auto_now_add=True)
    updateDate = models.DateTimeField(max_length=20, db_column='update_date', auto_now_add=True)

    objects = ModelManager()

    class Meta:
        db_table = 't_user_role'
