# -*- coding:utf-8 -*-
from django.urls import path
from . import views

# 设置命名空间名称
app_name = 'customer'

urlpatterns = [
    path('select_cname_and_lname_and_uname/', views.select_cname_and_lname_and_uname,
         name='select_cname_and_lname_and_uname'),
    path('select_link_phone_by_id/', views.select_link_phone_by_id, name='select_link_phone_by_id'),
    path('customer_index/', views.customer_index, name='customer_index'),
    path('select_customer_list/', views.select_customer_list, name='select_customer_list'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('select_customer_by_id/', views.select_customer_by_id, name='select_customer_by_id'),
    path('update_customer/', views.update_customer, name='update_customer'),
    path('delete_customer/', views.delete_customer, name='delete_customer'),
    path('linkman_index/', views.linkman_index, name='linkman_index'),
    path('select_linkman_by_customer_id/<int:c_id>/', views.select_linkman_by_customer_id,
         name='select_linkman_by_customer_id'),
    path('create_linkman/<int:c_id>/', views.create_linkman, name='create_linkman'),
    path('update_linkman/', views.update_linkman, name='update_linkman'),
    path('delete_linkman/', views.delete_linkman, name='delete_linkman'),
    path('contact_index/', views.contact_index, name='contact_index'),
    path('select_contact_by_customer_id/<int:c_id>/', views.select_contact_by_customer_id,
         name='select_contact_by_customer_id'),
    path('create_contact/<int:c_id>/', views.create_contact, name='create_contact'),
    path('update_contact/', views.update_contact, name='update_contact'),
    path('delete_contact/', views.delete_contact, name='delete_contact'),
    path('order_index/', views.order_index, name='order_index'),
    path('select_order_by_customer_id/<int:c_id>/', views.select_order_by_customer_id,
         name='select_order_by_customer_id'),
    path('select_order_by_id/', views.select_order_by_id, name='select_order_by_id'),
    path('select_order_detail_by_order_id/<int:order_id>/', views.select_order_detail_by_order_id,
         name='select_order_detail_by_order_id'),
    path('loss_index/', views.loss_index, name='loss_index'),
    path('select_loss/', views.select_loss, name='select_loss'),
    path('reprieve_index/', views.reprieve_index, name='reprieve_index'),
    path('select_reprieve_by_loss_id/<int:loss_id>/', views.select_reprieve_by_loss_id, name='select_reprieve_by_loss_id'),
    path('create_reprieve/<int:loss_id>/', views.create_reprieve, name='create_reprieve'),
    path('update_reprieve/', views.update_reprieve, name='update_reprieve'),
    path('delete_reprieve/', views.delete_reprieve, name='delete_reprieve'),
    path('ok_reprieve/', views.ok_reprieve, name='ok_reprieve'),
    path('select_customer_name/', views.select_customer_name, name='select_customer_name')
]
