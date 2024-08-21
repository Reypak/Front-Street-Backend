from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum, Q, F
from django.utils.dateparse import parse_date
from fs_applications.models import Application
from fs_loans.models import Loan
from fs_transactions.models import Transaction
from fs_utils.constants import ACCEPTED, ACTIVE, APPROVED, CANCELLED, CLOSED, DISBURSEMENT, MISSED, OVERDUE, PENDING, REJECTED, REPAYMENT


def get_overdue():
    """Returns total overdue amounts and counts"""

    principal = F('installments__principal')
    interest = F('installments__interest')
    paid_amount = F('installments__paid_amount')
    # total_charges = F('charge_penalties__amount')
    total_amount = principal + interest

    return Loan.objects.filter(status=ACTIVE).aggregate(
        total_overdue=Sum(
            total_amount - paid_amount,
            filter=Q(installments__status__in=[OVERDUE, MISSED])
        ),
        total_outstanding=Sum(
            total_amount-paid_amount,
        ),
    )


def get_transactions(start_date, end_date):
    """Returns total amount and counts of transactions"""

    date_filters = Q()

    if start_date:
        parsed_start_date = parse_date(start_date)
        date_filters &= Q(created_at__gte=parsed_start_date)
    if end_date:
        parsed_end_date = parse_date(end_date)
        date_filters &= Q(created_at__lte=parsed_end_date)

    return Transaction.objects.aggregate(
        disbursements=Count('id', filter=date_filters & Q(type=DISBURSEMENT)),
        repayments=Count('id', filter=date_filters & Q(type=REPAYMENT)),
        total_disbursed=Sum('amount', filter=date_filters &
                            Q(type=DISBURSEMENT)),
        total_repaid=Sum('amount', filter=date_filters & Q(type=REPAYMENT))
    )


def get_loan_counts(start_date, end_date):
    """Returns total amount and counts of Loans"""

    # Date filters
    date_filters = {
        ACTIVE: Q(),
        APPROVED: Q(),
        PENDING: Q()
    }

    if start_date:
        parsed_start_date = parse_date(start_date)
        date_filters[ACTIVE] &= Q(
            disbursement_date__gte=parsed_start_date)
        date_filters[APPROVED] &= Q(approved_date__gte=parsed_start_date)
        date_filters[PENDING] &= Q(created_at__gte=parsed_start_date)

    if end_date:
        parsed_end_date = parse_date(end_date)
        date_filters[ACTIVE] &= Q(disbursement_date__lte=parsed_end_date)
        date_filters[APPROVED] &= Q(approved_date__lte=parsed_end_date)
        date_filters[PENDING] &= Q(created_at__lte=parsed_end_date)

        # Perform a single query to get the counts
    loan_counts = Loan.objects.aggregate(
        active=Count(
            'id', filter=date_filters[ACTIVE] & Q(status=ACTIVE)),
        approved=Count(
            'id', filter=date_filters[APPROVED] & Q(status=APPROVED)),
        pending=Count(
            'id', filter=date_filters[PENDING] & Q(status=PENDING)),
        cancelled=Count('id', filter=Q(status=CANCELLED)),
        closed=Count('id', filter=Q(status=CLOSED)),
        overdue=Count('id', filter=Q(is_overdue=True)),
        total=Count('id')
    )
    return loan_counts


def get_application_counts(start_date, end_date):
    """Returns total amount and counts of Applications"""

    # Date filters
    date_filters = {
        PENDING: Q(),
        ACCEPTED: Q(),
        REJECTED: Q(),
    }

    if start_date:
        parsed_start_date = parse_date(start_date)
        date_filters[PENDING] &= Q(created_at__gte=parsed_start_date)

    if end_date:
        parsed_end_date = parse_date(end_date)
        date_filters[PENDING] &= Q(created_at__lte=parsed_end_date)

        # Perform a single query to get the counts
    counts = Application.objects.aggregate(
        pending=Count(
            'id', filter=date_filters[PENDING] & Q(status=PENDING)),
        accepted=Count(
            'id', filter=date_filters[ACCEPTED] & Q(status=ACCEPTED)),
        rejected=Count(
            'id', filter=date_filters[REJECTED] & Q(status=REJECTED)),
        total=Count('id')
    )
    return counts


def get_loan_categories():
    """Returns the list of all loan categories an total count"""
    loan_categories = Loan.objects.values(
        name=F('category__name')).annotate(total=Count('id'))
    return loan_categories


class ReportSummary(APIView):
    def get(self, request):
        # Parse the query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        return Response({
            'applications': get_application_counts(start_date, end_date),
            'loans': get_loan_counts(start_date, end_date),
            'categories': get_loan_categories(),
            'overdue': get_overdue(),
            'transactions': get_transactions(start_date, end_date),
        })
