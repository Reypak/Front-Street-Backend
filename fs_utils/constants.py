from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 5


# filter expressions
ICONTAINS = "icontains"
IEXACT = "iexact"

# actions
UPDATED = "updated"
CREATED = "created"

# statuses
PENDING = "pending"
APPROVED = "approved"
DECLINED = "declined"
DISBURSED = "disbursed"
CLOSED = "closed"
CANCELLED = "cancelled"
ACCEPTED = "accepted"

# installment status
OVERDUE = "overdue"
PAID = "paid"
NOT_PAID = "not_paid"
PARTIALLY_PAID = "partially_paid"
MISSED = "missed"

# loan types
DAILY = "daily"
WEEKLY = "weekly"
MONTHLY = "monthly"

# document types
DOCUMENT_TYPE_OTHER = "other"
DOCUMENT_TYPE_ATTACHMENT = "attachment"

# repayment types
FIXED_MONTHLY = "fixed_monthly"
INTEREST_ONLY = "interest_only"


# CHOICES
DOCUMENT_TYPES = (
    (DOCUMENT_TYPE_OTHER, 'Other'),
    (DOCUMENT_TYPE_ATTACHMENT, 'Attachment'),
)

LOAN_STATUSES = (
    (PENDING, 'Pending'),
    (APPROVED, 'Approved'),
    (CANCELLED, 'Cancelled'),
    (DISBURSED, 'Disbursed'),
    (CLOSED, 'Closed')
)

INSTALLMENT_CHOICES = (
    (PAID, 'Paid'),
    (NOT_PAID, 'Not Paid'),
    (PARTIALLY_PAID, 'Partially Paid'),
    (MISSED, 'Missed'),
)

# PAYMENT FREQUENCY
PAYMENT_FREQUENCY_CHOICES = [
    (DAILY, 'Daily'),
    (WEEKLY, 'Weekly'),
    (MONTHLY, 'Monthy'),
]

# REPAYMENT TYPES
REPAYMENT_TYPES = [
    (FIXED_MONTHLY, 'Fixed Monthly Payments'),
    (INTEREST_ONLY, 'Interest-Only Payments'),
]

# APPLICATION_STATUS
APPLICATION_STATUS_CHOICES = (
    (PENDING, 'Pending'),
    (ACCEPTED, 'Accepted'),
    (DECLINED, 'Declined'),
    (CANCELLED, 'Cancelled'),
)
