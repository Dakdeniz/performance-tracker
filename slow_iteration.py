import random
from celery import Celery
from account import tasks
import django
from django.conf import settings
import os
from datetime import date

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "performance_tracker.settings")
django.setup()

from account.models import DailyPerformance


app = Celery(
    "account.tasks",
    broker="redis://127.0.0.1:6379",
)


def run():

    dp_list = []
    for i in range(100):
        cost = random.uniform(100.0, 110.0)
        revenue = random.uniform(110.0, 150.0)
        profit = revenue - cost

        daily_performance = DailyPerformance(
            cost=100, revenue=revenue, profit=profit, date=date(2022, 8, 31)
        )

        dp_list.append(daily_performance)
    qs = DailyPerformance.objects.bulk_create(dp_list)
    tasks.iterate_daily_qs.delay()


if __name__ == "__main__":
    run()
