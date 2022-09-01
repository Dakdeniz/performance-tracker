from django.db import models
from django.db.models import ExpressionWrapper, F, FloatField, Case, When
from django.db.models.functions import Cast
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal


class PerformanceQuerySet(QuerySet):
    ...


class PerformanceManager(models.Manager):
    def filter_by_min_roi(self, min_roi: float):
        qs = self.get_queryset().annotate(
            roi=Case(
                When(cost=0.0, then=0.0),
                default=Cast(F("profit"), FloatField()) / Cast(F("cost"), FloatField()),
                output_fields=FloatField(),
            )
        )
        return qs.filter(roi__gt=min_roi)


class Performance(models.Model):
    """Abstract model for Performance data"""

    created_at = models.DateField(_("Creation date"), auto_now_add=True)
    cost = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    revenue = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    profit = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    objects = PerformanceManager()

    def save(self, *args, **kwargs):
        self.profit = self.revenue - self.cost
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class HourlyPerformance(Performance):
    datetime = models.DateTimeField()


class DailyPerformance(Performance):
    date = models.DateField()
