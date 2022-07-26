from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('loginLocMana/', TemplateView.as_view(template_name='loginLocationMana.html')),
    path('modifyPDHTML/', TemplateView.as_view(template_name='modifyPD.html'), name='modifyPDHTML'),

    path('log_success_failure/', views.log_success_failure, name='log_success_failure'),  # 用户登录成功和失败统计
    path('solve_log_failure/', views.solve_log_failure, name='solve_log_failure'),  # 处理登录失败的信息
    path('get_now_info/', views.get_now_info, name='get_now_info'),  # 得到当前的登录信息
    path('verify_logLocation/', views.verify_logLocation, name='verify_logLocation'),  # 验证登录位置信息

    path('verify_loc_modifyPD/', views.verify_loc_modifyPD, name='verify_loc_modifyPD'),  # 修改密码验证信息
    path('modifyPD/', views.modifyPD, name='modifyPD'),  # 修改密码
    path('sendMessage/', views.sendMessage, name='sendMessage'),  # 发送验证码

    path('searchLoginInfo/', views.searchLoginInfo, name='searchLoginInfo'),  # 查询功能
    path('get_authIp_info/', views.get_authIp_info, name='get_authIp_info'),  # 授权IP功能
]
