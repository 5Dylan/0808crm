# -*- coding:utf-8 -*-
from django.urls import path
from . import views

# 设置命名空间名称
app_name = 'serve'

urlpatterns = [
    path('serve/<str:serve_type>/', views.serve_index, name='serve'),
    path('create_serve/', views.create_serve, name='create_serve'),
    path('update_serve/', views.update_serve, name='update_serve'),
    path('select_serve/', views.select_serve, name='select_serve')
]
