from django.contrib import admin
from fs_categories.models import Category
from fs_installments.models import Installment
from fs_payments.models import LoanPayment
from fs_documents.models import Document
from fs_reports.models import LoanReport
from fs_loans.models import Loan
from fs_users.models import CustomUser
from fs_roles.models import Role
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(Loan)
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Document)
admin.site.register(LoanReport)
admin.site.register(Installment)
admin.site.register(LoanPayment)
admin.site.register(Role)
admin.site.register(Permission)
