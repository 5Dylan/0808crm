# -*- coding:utf-8 -*-
from django.urls import path
from . import views

# 设置命名空间名称
app_name = 'system'

urlpatterns = [
    path('login_register/', views.login_register, name='login_register'),
    path('system/unique_username/', views.unique_username, name='unique_username'),
    path('system/unique_email/', views.unique_email, name='unique_email'),
    path('system/send_email/', views.send_email, name='send_email'),
    path('system/active_accounts/', views.active_accounts, name='active_accounts'),
    path('system/login_user/', views.login_user, name='login_user'),
    path('index/', views.index, name='index'),
    path('system/update_password/', views.update_password, name='update_password'),
    path('system/logout/', views.logout, name='logout'),
    path('system/select_customer_manager/', views.select_customer_manager, name='select_customer_manager'),
    path('system/module_index/', views.module_index, name='module_index'),
    path('system/select_module/', views.select_module, name='select_module'),
    path('system/select_module_by_grade/', views.select_module_by_grade, name='select_module_by_grade'),
    path('system/create_module/', views.create_module, name='create_module'),
    path('system/update_module/', views.update_module, name='update_module'),
    path('system/delete_module/', views.delete_module, name='delete_module'),
    path('system/roel_index/', views.roel_index, name='roel_index'),
    path('system/select_role/', views.select_role, name='select_role'),
    path('system/create_role/', views.create_role, name='create_role'),
    path('system/update_role/', views.update_role, name='update_role'),
    path('system/delete_role/', views.delete_role, name='delete_role'),
    path('system/role_module_index/', views.role_module_index, name='role_module_index'),
    path('system/role_relate_module/', views.role_relate_module, name='role_relate_module'),
    path('system/user_index/', views.user_index, name='user_index'),
    path('system/select_user/', views.select_user, name='select_user'),
    path('system/select_role_for_user/', views.select_role_for_user, name='select_role_for_user'),
    path('system/create_user/', views.create_user, name='create_user'),
    path('system/select_role_by_userid/', views.select_role_by_userid, name='select_role_by_userid'),
    path('system/update_user/', views.update_user, name='update_user'),
    path('system/delete_user/', views.delete_user, name='delete_user')
]
