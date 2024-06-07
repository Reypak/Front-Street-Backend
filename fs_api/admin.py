from django.contrib import admin
from fs_installments.models import Installment
from fs_payments.models import LoanPayment
from fs_loan_types.models import LoanType
from fs_documents.models import Document
from fs_reports.models import LoanReport
from fs_loans.models import Loan

# Register your models here.
admin.site.register(Loan)
admin.site.register(LoanType)
admin.site.register(Document)
admin.site.register(LoanReport)
admin.site.register(Installment)
admin.site.register(LoanPayment)
