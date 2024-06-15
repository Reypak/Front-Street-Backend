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

OVERDUE = "overdue"
PAID = "paid"
PAST_DUE = "past_due"
CURRENT = "current"

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
    (PAST_DUE, 'Past Due'),
    (CURRENT, 'Current'),
    (OVERDUE, 'Overdue')
)

# LOAN TYPES
LOAN_TYPES = [
    (DAILY, 'Daily'),
    (WEEKLY, 'Weekly'),
    (MONTHLY, 'Monthy'),
]
