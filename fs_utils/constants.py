from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 5


# actions
UPDATED = "updated"
CREATED = "created"

# statuses
PENDING = "pending"
APPROVED = "approved"
DECLINED = "declined"
DISBURSED = "disbursed"
CLOSED = "closed"

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

DOCUMENT_TYPES = (
    (DOCUMENT_TYPE_OTHER, 'Other'),
    (DOCUMENT_TYPE_ATTACHMENT, 'Attachment'),
)

LOAN_STATUSES = (
    (PENDING, 'Pending'),
    (APPROVED, 'Approved'),
    (DECLINED, 'Declined'),
    (DISBURSED, 'Disbursed'),
    (CLOSED, 'Closed')
)

INSTALLMENT_CHOICES = (
    (PAID, 'Paid'),
    (NOT_PAID, 'Not Paid'),
    (PARTIALLY_PAID, 'Partially Paid'),
    (MISSED, 'Missed'),
)

# LOAN TYPES
LOAN_TYPES = [
    (DAILY, 'Daily'),
    (WEEKLY, 'Weekly'),
    (MONTHLY, 'Monthy'),
]
