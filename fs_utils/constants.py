from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class CustomPagination(PageNumberPagination):
    page_size = 5


# App name
APP_NAME = 'Front Street Lender'

# filter expressions
ICONTAINS = "icontains"
IEXACT = "iexact"
EXACT = "exact"

# actions
UPDATED = "updated"
CREATED = "created"

# statuses
PENDING = "pending"
APPROVED = "approved"
DECLINED = "declined"
DISBURSED = "disbursed"
ACTIVE = "active"
CLOSED = "closed"
CANCELLED = "cancelled"
ACCEPTED = "accepted"
REJECTED = "rejected"

# installment status
OVERDUE = "overdue"
PAID = "paid"
NOT_PAID = "not_paid"
PARTIALLY_PAID = "partially_paid"
MISSED = "missed"
WRITTEN_OFF = "written_off"

# loan types
DAILY = "daily"
WEEKLY = "weekly"
MONTHLY = "monthly"

# TRANSACTION TYPES
DISBURSEMENT = "disbursement"
REPAYMENT = "repayment"


# document types
DOCUMENT_TYPE_OTHER = "other"
DOCUMENT_TYPE_ATTACHMENT = "attachment"

# repayment types
FIXED_INTEREST = "fixed_interest"
INTEREST_ONLY = "interest_only"


# CHOICES
DOCUMENT_TYPES = (
    (DOCUMENT_TYPE_OTHER, 'Other'),
    (DOCUMENT_TYPE_ATTACHMENT, 'Attachment'),
)

LOAN_STATUSES = (
    (PENDING, 'Pending'),
    (APPROVED, 'Approved'),
    (ACTIVE, 'Active'),
    (CANCELLED, 'Cancelled'),
    (CLOSED, 'Closed')
)

INSTALLMENT_CHOICES = (
    (PAID, 'Paid'),
    (NOT_PAID, 'Not Paid'),
    (OVERDUE, 'Overdue'),
    (PARTIALLY_PAID, 'Partially Paid'),
    (MISSED, 'Missed'),
    (WRITTEN_OFF, 'Written Off'),
)

# TRANSACTION_CHOICES
TRANSACTION_CHOICES = (
    (DISBURSEMENT, 'Disbursement'),
    (REPAYMENT, 'Repayment'),
)

# PAYMENT FREQUENCY
PAYMENT_FREQUENCY_CHOICES = [
    (DAILY, 'Daily'),
    (WEEKLY, 'Weekly'),
    (MONTHLY, 'Monthy'),
]

# REPAYMENT TYPES
REPAYMENT_TYPES = [
    (FIXED_INTEREST, 'Fixed Interest'),
    (INTEREST_ONLY, 'Interest-Only'),
]

# APPLICATION_STATUS
APPLICATION_STATUS_CHOICES = (
    (PENDING, 'Pending'),
    (ACCEPTED, 'Accepted'),
    (REJECTED, 'Rejected'),
    (CANCELLED, 'Cancelled'),
)

# MONTH DAYS
MONTH_DAYS = 30

SENDER_NAME = APP_NAME
SENDER_EMAIL = settings.EMAIL_HOST_USER
FROM_EMAIL = f"{SENDER_NAME} <{SENDER_EMAIL}>"

# SECRET TOKEN
SECRET_TOKEN = "c2yFLZan1gRC50wBlGLLYECDCmXgaX8fYg1nctTALa4"
