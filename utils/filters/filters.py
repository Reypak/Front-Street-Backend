import django_filters
from loans.models import Loan


class LoanFilterSet(django_filters.FilterSet):
    borrower_name = django_filters.CharFilter(lookup_expr="icontains")
    category = django_filters.CharFilter(lookup_expr="exact")
    # field name
    category_name = django_filters.CharFilter(
        field_name="category__name", lookup_expr="icontains")

    class Meta:
        model = Loan
        fields = ['borrower_name', 'category', 'category_name']
