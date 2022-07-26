from django.contrib import admin
from login.models import *

# Register your models here.
admin.site.site_header = '后台管理系统'
admin.site.site_title = '后台管理系统'
admin.site.register(userInfo)


# @admin.register(userInfo)
# class userInfoAdmin(admin.ModelAdmin):
    # date_hierarchy = 'pub_date'