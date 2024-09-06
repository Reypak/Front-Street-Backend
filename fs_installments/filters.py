import django_filters
from .models import *
from django.utils import timezone
from datetime import date, timedelta


class InstallmentFilterSet(django_filters.FilterSet):
    due_date = django_filters.DateFromToRangeFilter()
    period = django_filters.CharFilter(method='filter_by_period')
    loan_status = django_filters.CharFilter(field_name='loan__status')

    class Meta:
        model = Installment
        fields = '__all__'

    def filter_by_period(self, queryset, name, value):
        # Get the current date
        # today = timezone.now().date()
        today = date.today()

        if value == 'today':
            # Filter installments due today
            return queryset.filter(due_date=today)
        elif value == 'tomorrow':
            # Filter installments due tomorrow
            return queryset.filter(due_date=today + timedelta(days=1))
        elif value == 'current_week':
            # Calculate the start of the current week (assuming week starts on Monday)
            week_start = today - timedelta(days=(today.weekday() + 1) % 7)
            # Calculate the end of the current week (Sunday)
            week_end = week_start + timedelta(days=6)
            # Filter installments due within the current week
            return queryset.filter(due_date__range=[week_start, week_end])
        elif value == 'current_month':
            # Calculate the start of the current month
            month_start = today.replace(day=1)
            # Calculate the start of the next month
            next_month = month_start + timedelta(days=32)
            # Calculate the end of the current month
            month_end = next_month.replace(day=1) - timedelta(days=1)
            # Filter installments due within the current month
            return queryset.filter(due_date__range=[month_start, month_end])

        # If no valid period is specified, return the original queryset
        return queryset
