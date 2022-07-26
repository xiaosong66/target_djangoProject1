from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('loginAUTH/', views.loginAUTH),    # 登录认证功能
    path('createUser/', views.createUser, name='createUser'),  # 新建用户
    path('logOut/', views.logOut),          # 退出登录函数
    path('get_user_info/', views.get_user_info),  # 获取用户个人的信息
    path('save_user_info/', views.save_user_info),  # 保存用户的信息
    path('statistics_log_info/', views.statistics_log_info, name='statistics_log_info'),  # 统计用户登录位置信息
    path('log_info/', views.log_info, name='log_info'),  # index页面的简略信息


    path('sendMessage/<type>/', views.sendMessage, name='sendMessage'),  # 发送邮件
    path('verifyAuthCode/', views.verifyAuthCode, name='verifyAuthCode'),  # 验证异地登录的验证码
    path('modify_PD/', views.modify_PD, name='modify_PD'),  # 修改密码


    path('login/', TemplateView.as_view(template_name="login.html")),  # 登录页面
    path('register/', TemplateView.as_view(template_name="register.html")),     # 注册页面
    path('indiInfo/', TemplateView.as_view(template_name="individualInfo.html")),  # 用户中心
    path('judge_userInfo_integrity/', views.judge_userInfo_integrity),  # 判断用户信息是否完整

]
