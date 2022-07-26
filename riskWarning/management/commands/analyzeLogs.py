# -*- coding: utf-8 -*-
# @Time    : 2022/5/25 21:00
# @Author  : xiaosong
# @File    : analyzeLogs.py
# @Software: PyCharm
import logging
import os.path
import datetime

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from target_djangoProject1.settings import BASE_DIR
from riskWarning.models import *

# 初始化日志对象
logger = logging.getLogger(__name__)


# 获取昨天日志目录
def get_log_Path():
    # 获取昨天日志的日期，按天划分
    today = datetime.datetime.today()
    oneday = datetime.timedelta(days=1)
    yesterday = (today - oneday).strftime("%Y-%m-%d")

    # 获取日志
    yesterday_logName = 'web-log.log.' + yesterday
    logPath = os.path.join(BASE_DIR, 'logs\\accessLogs', yesterday_logName)
    return logPath

# 分析日志
def analyzeLogs():

    logPath = get_log_Path()  # 日志路径
    file_obj = open(logPath, 'r')

    status_codes = ['404']  # 检索范围
    accessPaths = ['/lg/login/', '/LM/modifyPDHTML/', '/lg/modify_PD/', '/lg/loginAUTH/']
    try:
        for i in file_obj:
            i = eval(i)  # 转为字典类型数据
            if (i['status_code'] in status_codes) or (i['path'] in accessPaths):
                # 存入数据库
                data = accessLogs(time=i['time'], level=i['level'], method=i['method'],
                                  username=i['username'], sip=i['sip'], dip=i['dip'],
                                  path=i['path'], status_code=i['status_code'],
                                  reason_phrase=i['reason_phrase'])
                data.save()
    finally:
        print("特定日志取出完毕")
        file_obj.close()

class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            # 添加定时任务
            analyzeLogs,
            #  '*/' 表示每多久
            # trigger=CronTrigger(hour="00", minute="00", second="00"),  # 每天00:00
            trigger=CronTrigger(second="*/30"),  # Every 1 hour
            id="disposeAccessLog",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )

        logger.info("Added job 'disposeAccessLog'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
