import django_filters
from fs_loan_reports.models import LoanReport
from loans.models import Loan

ICONTAINS = "icontains"
IEXACT = "iexact"


class LoanFilterSet(django_filters.FilterSet):
    borrower_name = django_filters.CharFilter(lookup_expr=ICONTAINS)
    loan_type = django_filters.CharFilter(lookup_expr=IEXACT)
    # field name
    loan_type_name = django_filters.CharFilter(
        field_name="loan_type__name", lookup_expr=ICONTAINS)

    class Meta:
        model = Loan
        fields = ['borrower_name', 'loan_type', 'loan_type_name']


class LoanReportFilterSet(django_filters.FilterSet):
    action = django_filters.CharFilter(lookup_expr=IEXACT)
    status = django_filters.CharFilter(lookup_expr=IEXACT)

    class Meta:
        model = LoanReport
        fields = ['status', 'action']
