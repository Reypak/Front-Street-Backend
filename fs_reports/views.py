import calendar
from django.db.models.functions import TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum, Q, F
from django.utils.dateparse import parse_date
from fs_applications.models import Application
from fs_loans.models import Loan
from fs_transactions.models import Transaction
from fs_users.models import CustomUser
from fs_utils.constants import ACCEPTED, ACTIVE, APPROVED, CANCELLED, CLOSED, DISBURSED, DISBURSEMENT, MISSED, OVERDUE, PENDING, REJECTED, REPAYMENT, WRITTEN_OFF


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
        DISBURSED: Q(),
        APPROVED: Q(),
        PENDING: Q()
    }

    if start_date:
        parsed_start_date = parse_date(start_date)
        date_filters[DISBURSED] &= Q(
            disbursement_date__gte=parsed_start_date)
        date_filters[APPROVED] &= Q(approved_date__gte=parsed_start_date)
        date_filters[PENDING] &= Q(created_at__gte=parsed_start_date)

    if end_date:
        parsed_end_date = parse_date(end_date)
        date_filters[DISBURSED] &= Q(disbursement_date__lte=parsed_end_date)
        date_filters[APPROVED] &= Q(approved_date__lte=parsed_end_date)
        date_filters[PENDING] &= Q(created_at__lte=parsed_end_date)

        # Perform a single query to get the counts
    loan_counts = Loan.objects.aggregate(
        active=Count('id', filter=Q(status=ACTIVE)),
        disbursed=Count(
            'id', filter=date_filters[DISBURSED] & Q(status=ACTIVE)),
        approved=Count(
            'id', filter=date_filters[APPROVED] & Q(status=APPROVED)),
        pending=Count(
            'id', filter=date_filters[PENDING] & Q(status=PENDING)),
        cancelled=Count('id', filter=Q(status=CANCELLED)),
        closed=Count('id', filter=Q(status=CLOSED)),
        overdue=Count('id', filter=Q(is_overdue=True)),
        written_off=Count('id', filter=Q(status=WRITTEN_OFF)),
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
        date_filters[ACCEPTED] &= Q(loan__created_at__gte=parsed_start_date)

    if end_date:
        parsed_end_date = parse_date(end_date)
        date_filters[PENDING] &= Q(created_at__lte=parsed_end_date)
        date_filters[ACCEPTED] &= Q(loan__created_at__lte=parsed_end_date)

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


def get_application_amounts(start_date, end_date):
    """Returns application amounts"""

    date_filters = {
        PENDING: Q(),
        ACCEPTED: Q(),
    }

    if start_date:
        parsed_start_date = parse_date(start_date)
        date_filters[PENDING] &= Q(created_at__gte=parsed_start_date)
        date_filters[ACCEPTED] &= Q(loan__created_at__gte=parsed_start_date)

    if end_date:
        parsed_end_date = parse_date(end_date)
        date_filters[PENDING] &= Q(created_at__lte=parsed_end_date)
        date_filters[ACCEPTED] &= Q(loan__created_at__lte=parsed_end_date)

    amounts = Application.objects.aggregate(
        total_requested=Sum(
            'amount', filter=date_filters[PENDING] & Q(status=PENDING)),
        total_approved=Sum(
            'amount', filter=date_filters[ACCEPTED] & Q(status=ACCEPTED)),
    )

    return amounts


def get_loan_categories():
    """Returns the list of all loan categories an total count"""
    loan_categories = Loan.objects.values(
        name=F('category__name')).annotate(total=Count('id'))
    return loan_categories


def get_users(start_date, end_date):
    """Returns the list of all loan categories an total count"""

    date_filters = Q()

    if start_date:
        parsed_start_date = parse_date(start_date)
        date_filters &= Q(date_joined__gte=parsed_start_date)
    if end_date:
        parsed_end_date = parse_date(end_date)
        date_filters &= Q(date_joined__lte=parsed_end_date)

    counts = CustomUser.objects.aggregate(
        clients=Count(
            'id', filter=date_filters & Q(is_staff=False)),
        staff=Count(
            'id', filter=date_filters & Q(is_staff=True)),
        total=Count('id')
    )
    return counts


def get_transactions_by_month():
    # Aggregate transactions by month
    monthly_performance = (
        Transaction.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(
            total_disbursed=Sum('amount', filter=Q(type=DISBURSEMENT)),
            total_repaid=Sum('amount', filter=Q(type=REPAYMENT))
        )
        .order_by('month')
    )

    # Prepare the response data with month label
    data = []
    for record in monthly_performance:
        month = record['month']

        # Get the month name and year
        month_name = f"{calendar.month_name[month.month]}"
        year = f"{month.year}"

        data.append({
            "month": month_name,
            "year": year,
            "total_disbursed": record['total_disbursed'] or 0,
            "total_repaid": record['total_repaid'] or 0,
        })

    return data


class ReportSummary(APIView):
    def get(self, request):
        # Parse the query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        return Response({
            'applications': {
                'counts': get_application_counts(start_date, end_date),
                'amounts': get_application_amounts(start_date, end_date)
            },
            'loans': {'counts': get_loan_counts(start_date, end_date),
                      'categories': get_loan_categories(),
                      },
            'overdue': get_overdue(),
            'transactions': get_transactions(start_date, end_date),
            'transactions_by_month': get_transactions_by_month(),
            'users': get_users(start_date, end_date)
        })
