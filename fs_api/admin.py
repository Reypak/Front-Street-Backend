from django.contrib import admin
from fs_loan_types.models import LoanType
from documents.models import Document
from fs_loan_reports.models import LoanReport
from loans.models import Loan

# Register your models here.
admin.site.register(Loan)
admin.site.register(LoanType)
admin.site.register(Document)
admin.site.register(LoanReport)
