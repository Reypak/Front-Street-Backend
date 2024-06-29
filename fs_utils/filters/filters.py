import django_filters
from fs_payments.models import LoanPayment
from fs_reports.models import LoanReport
from fs_utils.constants import ICONTAINS, IEXACT


class LoanReportFilterSet(django_filters.FilterSet):
    action = django_filters.CharFilter(lookup_expr=IEXACT)
    status = django_filters.CharFilter(lookup_expr=IEXACT)

    class Meta:
        model = LoanReport
        fields = ['status', 'action']


class LoanPaymentFilterSet(django_filters.FilterSet):
    application_number = django_filters.CharFilter(
        lookup_expr=IEXACT,  field_name="loan__application_number")
    borrower_name = django_filters.CharFilter(
        field_name="loan__borrower_name", lookup_expr=ICONTAINS)

    class Meta:
        model = LoanPayment
        fields = ['borrower_name', 'application_number']
