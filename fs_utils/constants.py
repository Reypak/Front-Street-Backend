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
DUE_TODAY = "due_today"
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
OTHER = "other"
DOCUMENT_TYPE_ATTACHMENT = "attachment"

# repayment types
FIXED_INTEREST = "fixed_interest"
INTEREST_ONLY = "interest_only"


# CHOICES
DOCUMENT_TYPES = (
    (OTHER, OTHER),
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
    (DUE_TODAY, DUE_TODAY),
    (PARTIALLY_PAID, 'Partially Paid'),
    (MISSED, 'Missed'),
    (WRITTEN_OFF, 'Written Off'),
)


CHARGE_CHOICES = (
    (PAID, PAID),
    (NOT_PAID, NOT_PAID),
    (PARTIALLY_PAID, PARTIALLY_PAID),
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

TRANSACTION = "transaction"
SCHEDULE = "schedule"
REMINDER = "reminder"
COMMENT = "comment"
LOAN = "loan"

CHARGE = "charge"
PENATLTY = "penalty"

ACTION_CHOICES = [
    ('create', 'Create'),
    ('update', 'Update'),
    ('delete', 'Delete'),
    (REPAYMENT, REPAYMENT),
    (TRANSACTION, TRANSACTION),
    (SCHEDULE, SCHEDULE),
    (REMINDER, REMINDER),
    (COMMENT, COMMENT),
    (CHARGE, CHARGE),
]


# CHARGE TYPES
CHARGE_CHOICES = [
    (CHARGE, CHARGE),
    (PENATLTY, PENATLTY),
    (OTHER, OTHER),
]

# CHARGE_PENALTY_CHOICES
CHARGE_PENALTY_CHOICES = [
    (NOT_PAID, NOT_PAID),
    (PARTIALLY_PAID, PARTIALLY_PAID),
    (PAID, PAID),
]

CORE = 'system-core'
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d(%H-%M)'
SITE_URL = 'http://localhost:3200/'

# PERMISSIONS
CAN_ADMIN = 'can_admin'
CAN_VIEW_TRANSACTION = 'view_transaction'
CAN_ADD_TRANSACTION = 'add_transaction'
CAN_CHANGE_APPLICATION_STATUS = "change_application_status"
CAN_CHANGE_LOAN_STATUS = "change_loan_status"


COMPLETED = 'completed'
# IN_PROGRESS = 'in_progress'

# TASK CHOICES
TASK_STATUS_CHOICES = [
    (PENDING, PENDING),
    # (IN_PROGRESS, IN_PROGRESS),
    (COMPLETED, COMPLETED),
    (CLOSED, CLOSED),
]
