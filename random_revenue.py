import os
import random
from datetime import date
from decimal import Decimal
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "performance_tracker.settings")
django.setup()

from account.models import DailyPerformance


def run():

    dp_list = []
    for i in range(100000):
        cost = 100
        revenue = random.uniform(100.0, 200.0)
        profit = revenue - cost

        daily_performance = DailyPerformance(
            cost=100, revenue=revenue, profit=profit, date=date(2022, 8, 31)
        )

        dp_list.append(daily_performance)
    qs = DailyPerformance.objects.bulk_create(dp_list)

    qs_roi = DailyPerformance.objects.filter_by_min_roi(min_roi=0.50)

    print("Length of filtered Queryset : ", qs_roi.count())
    print("Length of filtered Queryset multiplied by 2 : ", qs_roi.count() * 2)

    update(qs_roi)


def update(qs):
    index = 1
    total_count = qs.count()
    print(DailyPerformance.objects.values_list("revenue", flat=True))
    for dp in qs:
        print(f"Index of loop: {index}/{total_count}")

        old_revenue = dp.revenue
        dp.revenue = round(dp.revenue * Decimal(random.uniform(0.5, 2.0)), 2)
        dp.profit = dp.revenue - dp.cost
        print(f"Old revenue = {old_revenue} / New revenue = {dp.revenue}")
        # dp.save()
        index += 1

    DailyPerformance.objects.bulk_update(qs, ["revenue", "cost"], batch_size=200000)


if __name__ == "__main__":
    run()
    DailyPerformance.objects.all().delete()
