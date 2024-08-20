# from rest_framework import viewsets

# from fs_utils.filters.filter_backends import DEFAULT_FILTER_BACKENDS
# from fs_utils.filters.filters import LoanReportFilterSet
# from .serializers import LoanReportSerializer
# from .models import LoanReport
# from rest_framework.permissions import IsAuthenticated

# # Create your views here.


# class LoanReportViewSet(viewsets.ModelViewSet):
#     queryset = LoanReport.objects.all()
#     serializer_class = LoanReportSerializer
#     filter_backends = DEFAULT_FILTER_BACKENDS
#     filterset_class = LoanReportFilterSet
#     permission_classes = [IsAuthenticated]

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum, Q, F
from django.utils.dateparse import parse_date
from fs_loans.models import Loan
from fs_utils.constants import ACTIVE, APPROVED, CANCELLED, CLOSED, MISSED, OVERDUE, PENDING


def total_overdue_amount():
    return Loan.objects.filter(is_overdue=True, status=ACTIVE).aggregate(
        total_overdue=Sum(
            F('installments__principal') + F('installments__interest') -
            F('installments__paid_amount'),
            filter=Q(installments__status__in=[OVERDUE, MISSED])
        )
    )['total_overdue'] or 0


class ReportSummary(APIView):
    def get(self, request):
        # Parse the query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Date filters
        date_filters = {
            'active': Q(),
            'approved': Q(),
            'pending': Q()
        }

        if start_date:
            parsed_start_date = parse_date(start_date)
            date_filters['active'] &= Q(
                disbursement_date__gte=parsed_start_date)
            date_filters['approved'] &= Q(approved_date__gte=parsed_start_date)
            date_filters['pending'] &= Q(created_at__gte=parsed_start_date)

        if end_date:
            parsed_end_date = parse_date(end_date)
            date_filters['active'] &= Q(disbursement_date__lte=parsed_end_date)
            date_filters['approved'] &= Q(approved_date__lte=parsed_end_date)
            date_filters['pending'] &= Q(created_at__lte=parsed_end_date)

        # Perform a single query to get the counts
        loan_counts = Loan.objects.aggregate(
            active=Count(
                'id', filter=date_filters['active'] & Q(status=ACTIVE)),
            approved=Count(
                'id', filter=date_filters['approved'] & Q(status=APPROVED)),
            pending=Count(
                'id', filter=date_filters['pending'] & Q(status=PENDING)),
            cancelled=Count('id', filter=Q(status=CANCELLED)),
            closed=Count('id', filter=Q(status=CLOSED)),
            overdue=Count('id', filter=Q(is_overdue=True)),
        )

        return Response({'count': loan_counts, 'total': {
            'overdue': total_overdue_amount(), 'collected': 0, 'disbursed': 0,
            'outstanding': 0
        }})
