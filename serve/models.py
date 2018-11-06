from django.db import models


class ModelManager(models.Manager):

    def get_queryset(self):
        return super(ModelManager, self).get_queryset().filter(isValid=1)


# 服务模型
class CustomerServe(models.Model):
    # 服务类型 咨询/建议/投诉
    serveType = models.CharField(db_column='serve_type', max_length=30)
    # 概要
    overview = models.CharField(db_column='overview', max_length=500)
    # 客户
    customer = models.CharField(db_column='customer', max_length=30)
    # 新创建/已分配/已处理/已归档
    state = models.CharField(db_column='state', max_length=10)
    # 服务请求
    serviceRequest = models.CharField(db_column='service_request', max_length=500)
    # 创建人
    createPeople = models.CharField(db_column='create_people', max_length=100)
    # 分配人
    assigner = models.CharField(db_column='assigner', max_length=100)
    # 分配日期
    assignTime = models.DateTimeField(db_column='assign_time')
    # 服务处理
    serviceProce = models.CharField(db_column='service_proce', max_length=500)
    # 服务处理人
    serviceProcePeople = models.CharField(db_column='service_proce_people', max_length=50)
    # 服务处理日期
    serviceProceTime = models.DateTimeField(db_column='service_proce_time')
    # 服务处理结果
    serviceProceResult = models.CharField(db_column='service_proce_result', max_length=500)

    # 客户满意度
    myd = models.CharField(db_column='myd', max_length=50)
    isValid = models.IntegerField(db_column='is_valid', default=1)
    createDate = models.DateTimeField(db_column='create_date', auto_now_add=True)
    updateDate = models.DateTimeField(db_column='update_date', auto_now_add=True)
    objects = ModelManager()

    class Meta:
        db_table = 't_customer_serve'
