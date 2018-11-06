# -*- coding:utf-8 -*-
from django.urls import path
from . import views

# 设置命名空间名称
app_name = 'report'

urlpatterns = [
    path('contirbute_index/', views.contirbute_index, name='contirbute_index'),
    path('select_contirbute/', views.select_contirbute, name='select_contirbute'),
    path('composition_index/', views.composition_index, name='composition_index'),
    path('select_compostion/', views.select_compostion, name='select_compostion'),
    path('serve_index/', views.serve_index, name='serve_index'),
    path('select_serve/', views.select_serve, name='select_serve'),
    path('loss_index/', views.loss_index, name='loss_index')
]
