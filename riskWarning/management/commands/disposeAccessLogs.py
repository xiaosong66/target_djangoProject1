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


# 判断昨天的日志是否被保存取出
# 也可以判断日志文件是否存在
def judge_log_save():
    recordLogPath = os.path.join(BASE_DIR, 'logs\\accessLogs', 'web-log.log')
    modify_time = datetime.datetime.fromtimestamp(os.path.getmtime(recordLogPath)).strftime("%Y-%m-%d")
    # print(modify_time)
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    # print(today)
    # oneday = datetime.timedelta(days=1)
    # yesterday = (today - oneday).strftime("%Y-%m-%d")
    # 得到昨天日志记录的目录
    yesterday_logPath = get_log_Path()
    # print(yesterday_logPath)
    # print(modify_time)
    if today != modify_time:
        with open(recordLogPath, 'r') as f1:
            content = f1.read()
            with open(yesterday_logPath, 'a+') as f2:
                f2.write(content)
        with open(recordLogPath, 'w') as f3:
            f3.write('')
        print("日志取出完毕")
    print("还未到另一天")


# 定时分析日志任务
# 取出必要的日志，返回的特殊错误和特殊目录
def disposeAccessLog():
    judge_log_save()

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


# 删除过时任务
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    # 这个def主要是为了解决以前异步任务执行久了会导致max_age的问题
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            # 添加定时任务
            disposeAccessLog,
            #  '*/' 表示每多久
            # trigger=CronTrigger(hour="00", minute="00", second="00"),  # 每天00:00
            trigger=CronTrigger(second="*/30"),  # Every 1 hour
            id="disposeAccessLog",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )

        logger.info("Added job 'disposeAccessLog'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
