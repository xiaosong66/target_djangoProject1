from django.urls import path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('riskWarning/', TemplateView.as_view(template_name='riskWarning.html')),

    path('get_loginFailure_info/', views.get_loginFailure_info),  # 返回登录锁定信息

    path("getPdStrengthSecurityInfo/", views.getPdStrengthSecurityInfo, name='getPdStrengthSecurityInfo'),  # 获取密码强度信息
    path("getPropertySecurityInfo/", views.getPropertySecurityInfo, name='getPropertySecurityInfo'),  # 获取资产安全信息
    path("getOtherSecurityInfo/", views.getOtherSecurityInfo, name='getOtherSecurityInfo'),  # 获取授权安全信息
    path("getAccountSecurityInfo/", views.getAccountSecurityInfo, name='getAccountSecurityInfo'),  # 获取账户安全信息
    path("getActionSecurityInfo/", views.getActionSecurityInfo, name='getActionSecurityInfo'),  # 获取行为安全信息

    path("getSecurityScore/", views.getSecurityScore, name='getSecurityScore'),  # 获取总体安全评分
]
