from rest_framework import viewsets
from weasyprint import HTML
from fs_installments.models import Installment
from fs_loans.filters import LoanFilterSet
from fs_loans.permissions import LoanPermission
from django.http import HttpResponse
from django.template.loader import render_to_string
from datetime import datetime

from fs_utils.constants import ADDRESS_DETAILS, APP_NAME

# from utils.constants import CustomPagination

# Create your views here.
# import local data
from .serializers import *
from .models import Loan
# from rest_framework.permissions import IsAuthenticated

# create a viewset


class LoanViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = Loan.objects.all()
    permission_classes = [LoanPermission]

    # specify serializer to be used
    # serializer_class = LoanSerializer

    # set data filters
    filterset_class = LoanFilterSet

    def get_queryset(self):
        user = self.request.user
        if user.is_staff is True:
            # show all for staff
            queryset = Loan.objects.all()
        else:
            # only for user
            queryset = Loan.objects.filter(client=user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return LoanListSerializer
        if self.action == 'retrieve':
            return LoanViewSerializer

        return LoanSerializer

    # for custom pagination
    # pagination_class = CustomPagination

    # def perform_create(self, serializer):
    #     return serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(updated_by=self.request.user)


def download_loan_statement(request, loan_id):
    # Get the loan and its installments
    loan = Loan.objects.get(id=loan_id)
    installments = Installment.objects.filter(loan=loan)

    context = {
        'loan': loan,
        'installments': installments,
        'current_date': datetime.now().strftime('%Y-%m-%d'),
        'year': datetime.now().year,
        'app_name': APP_NAME,
        'address': ADDRESS_DETAILS,
        'payments': {
            'reference_number':  loan.ref_number,
            'disbursement_date': loan.disbursement_date,
            'end_date': loan.end_date,
            'overdue_amount': loan.overdue,
            'principal': loan.amount,
            'charges': loan.charges,
            'paid_amount': loan.amount_paid,
            'outstanding_balance': loan.outstanding_balance,
        },
        'accounts': {
            'interest_rate': loan.interest_rate,
            'interest_amount': loan.interest_amount,
            'loan_term': loan.loan_term,
            'status': loan.status,
        }
    }

    # Render the loan statement template
    html_string = render_to_string('loan_statement.html', context)

    # Convert the HTML to a PDF
    pdf_file = HTML(string=html_string).write_pdf()

    # Return the response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="loan_statement_{loan.ref_number}.pdf"'
    return response
