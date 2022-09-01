from time import sleep
import os
from celery import shared_task
from celery.utils.log import get_task_logger
import django
from django.conf import settings

logger = get_task_logger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "performance_tracker.settings")
django.setup()
from .models import DailyPerformance


@shared_task  # (ignore_result=True, bind=True)
def iterate_daily_qs():
    qs = DailyPerformance.objects.all()[:50]

    for dp in qs:

        sleep(60)
        logger.info(
            f"Daily Performance Values: Revenue:{dp.revenue} - Cost:{dp.cost} = Profit:{dp.profit}"
        )
    return
