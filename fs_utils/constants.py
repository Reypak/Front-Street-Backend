from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 5


# actions
UPDATED = "updated"
CREATED = "created"

# statuses
STATUS_PENDING = "pending"
STATUS_APPROVED = "approved"
STATUS_DECLINED = "declined"
STATUS_DISBURSED = "disbursed"
STATUS_CLOSED = "closed"

OVERDUE = "overdue"
PAID = "paid"
PAST_DUE = "past_due"
CURRENT = "current"

# document types
DOCUMENT_TYPE_OTHER = "other"
DOCUMENT_TYPE_ATTACHMENT = "attachment"

DOCUMENT_TYPES = (
    (DOCUMENT_TYPE_OTHER, 'Other'),
    (DOCUMENT_TYPE_ATTACHMENT, 'Attachment'),
)

LOAN_STATUSES = (
    (STATUS_PENDING, 'Pending'),
    (STATUS_APPROVED, 'Approved'),
    (STATUS_DECLINED, 'Declined'),
    (STATUS_DISBURSED, 'Disbursed'),
    (STATUS_CLOSED, 'Closed')
)

INSTALLMENT_CHOICES = (
    (PAID, 'Paid'),
    (PAST_DUE, 'Past Due'),
    (CURRENT, 'Current'),
    (OVERDUE, 'Overdue')
)
