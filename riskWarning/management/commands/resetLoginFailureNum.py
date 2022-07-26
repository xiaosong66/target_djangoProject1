import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from login.models import userInfo

logger = logging.getLogger(__name__)


# 每日重置用户登录失败次数为0
# 重置用户可登录状态
def resetLoginFailureNum():
    objs = userInfo.objects.all()
    for obj in objs:
        # 连续登录失败天数小于三天
        if obj.loginFailure_days < 3:
            obj.if_auth_login = True
            obj.login_failure_num = 0
            obj.loginFailure_days_Tag = 0
            obj.save()
    print("重置完毕")


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            resetLoginFailureNum,
            #  '*/' 表示每多久
            # trigger=CronTrigger(hour="00", minute="00", second="00"),  # 每天00:00
            trigger=CronTrigger(second="*/30"),  # Every 1 hour
            id="disposeAccessLog",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )

        logger.info("Added job 'resetLoginFailureNum'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
