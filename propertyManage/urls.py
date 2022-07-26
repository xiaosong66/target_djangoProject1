from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('property/', TemplateView.as_view(template_name="property.html")),

    path('add_data/', views.add_data),  # 添加数据
    path('get_all_data/', views.get_all_data),  # 获取全部数据
    path('search_data/', views.search_data, name='search_data'),  # 查询数据
    path('deleteAll/', views.deleteAll),  # 删除所有选中的数据
    path('deleteOne/', views.deleteOne),    # 删除一条数据
    path('editOne/', views.editOne),  # 修改一条数据

    path('downloadFile/', views.downloadFile),  # 下载文件

    path('judge_make_secondPD/', views.judge_make_secondPD),  # 检测是否设置二次密码
    path('setSecondPD/', views.setSecondPD, name='setSecondPD'),  # 设置二次密码

 ]
