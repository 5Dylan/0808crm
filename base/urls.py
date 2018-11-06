# -*- coding:utf-8 -*-
from django.urls import path
from . import views

# 设置命名空间名称
app_name = 'base'

urlpatterns = [
    path('select_customer_level/', views.select_customer_level, name='select_customer_level'),
    path('datadic_index/', views.datadic_index, name='datadic_index'),
    path('select_datadic/', views.select_datadic, name='select_datadic'),
    path('select_datadic_name/', views.select_datadic_name, name='select_datadic_name'),
    path('create_datadic/', views.create_datadic, name='create_datadic'),
    path('update_datadic/', views.update_datadic, name='update_datadic'),
    path('delete_datadic/', views.delete_datadic, name='delete_datadic'),
    path('product_index/', views.product_index, name='product_index'),
    path('select_product/', views.select_product, name='select_product'),
    path('create_product/', views.create_product, name='create_product'),
    path('update_product/', views.update_product, name='update_product'),
    path('delete_product/', views.delete_product, name='delete_product')
]
