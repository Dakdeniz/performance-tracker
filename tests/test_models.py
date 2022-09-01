import json
import random
from urllib.parse import urlencode

import pytest
from django.contrib.gis.geos.geometry import GEOSGeometry
from django.forms.models import model_to_dict
from model_bakery import baker

from account.models import DailyPerformance

pytestmark = pytest.mark.django_db


def test_daily_performance():

    dp = baker.make(DailyPerformance)
    assert isinstance(dp, DailyPerformance)
    assert dp.cost >= 0
    assert dp.revenue >= 0
    assert dp.profit == dp.revenue - dp.cost


def test_roi():

    quantity_20 = random.randint(1, 10)
    quantity_10 = random.randint(1, 10)

    baker.make(
        DailyPerformance,
        revenue=120,
        cost=100,
        _quantity=quantity_20,
    )
    baker.make(
        DailyPerformance,
        revenue=110,
        cost=100,
        _quantity=quantity_10,
    )

    qs_10 = DailyPerformance.objects.filter_by_min_roi(min_roi=0.10)
    qs_20 = DailyPerformance.objects.filter_by_min_roi(min_roi=0.20)

    assert qs_10.count() == quantity_10 + quantity_20
    assert qs_20.count() == quantity_20
