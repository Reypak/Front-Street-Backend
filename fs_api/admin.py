from django.contrib import admin
from categories.models import Category
from documents.models import Document

from loans.models import Loan

# Register your models here.
admin.site.register(Loan)
admin.site.register(Category)
admin.site.register(Document)
