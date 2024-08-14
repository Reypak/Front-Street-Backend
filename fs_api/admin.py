from django.contrib import admin
from fs_applications.models import Application
from fs_audits.models import AuditTrail
from fs_categories.models import Category
from fs_charges.models import Charge, ChargePenalty
from fs_comments.models import Comment
from fs_installments.models import Installment
from fs_documents.models import Document
from fs_loans.models import Loan
from fs_profiles.models import Profile
from fs_transactions.models import Transaction
from fs_users.models import CustomUser
from fs_roles.models import Role
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(Loan)
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Document)
admin.site.register(Installment)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(Application)
admin.site.register(Charge)
admin.site.register(ChargePenalty)
admin.site.register(Comment)
admin.site.register(Transaction)
admin.site.register(AuditTrail)
admin.site.register(Profile)
