from django.contrib import admin
from categories.models import Category

from loans.models import Loan

# Register your models here.
admin.site.register(Loan)
admin.site.register(Category)
