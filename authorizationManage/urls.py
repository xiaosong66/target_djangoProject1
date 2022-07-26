from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('authorization/', TemplateView.as_view(template_name='authorization.html')),

    # path('add_log_info/', views.add_log_info),  # 添加登录信息
    path('get_propertyAuth_info/', views.get_propertyAuth_info, name='get_propertyAuth_info'),  # 获取资产授权信息，index页面
    path('get_auth_ip/', views.get_auth_ip, name='get_auth_ip'),  # 获取授权的ip地址
    path('add_share_info/', views.add_share_info),  # 新增共享的信息

    path('modify_auth_IP/', views.modify_auth_IP, name='modify_auth_IP'),  # 修改ip授权信息
    path('add_new_authIP/', views.add_new_authIP, name='add_new_authIP'),  # 新增ip授权信息
    path('delete_auth_ip/', views.delete_auth_ip, name='delete_auth_ip'),  # 删除ip授权信息
    path('delete_selectAll_IP/', views.delete_selectAll_IP),  # 删除选中的授权IP

    path('delete_auth_property/', views.delete_auth_property),  # 删除授权的资产
    path('modify_auth_property/', views.modify_auth_property),  # 修改资产授权
    path('delete_selectAll_properties/', views.delete_selectAll_properties),  # 删除选中的授权资产
]
