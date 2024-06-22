import django_filters
from fs_loans.filters import BaseLoanFilterSet
from fs_payments.models import LoanPayment
from fs_reports.models import LoanReport
from fs_loans.models import Loan

ICONTAINS = "icontains"
IEXACT = "iexact"


class LoanFilterSet(BaseLoanFilterSet):
    application_number = django_filters.CharFilter(lookup_expr=IEXACT)
    borrower_name = django_filters.CharFilter(lookup_expr=ICONTAINS)
    category = django_filters.CharFilter(lookup_expr=IEXACT)
    loan_type = django_filters.CharFilter(lookup_expr=IEXACT)
    # field name
    category_name = django_filters.CharFilter(
        field_name="category__name", lookup_expr=ICONTAINS)

    class Meta:
        model = Loan
        fields = ['borrower_name',
                  'loan_type',
                  'category',
                  'category_name',
                  'application_number']


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
