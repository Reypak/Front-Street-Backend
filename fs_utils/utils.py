from datetime import datetime
import uuid

from fs_utils.constants import DAILY, MONTH_DAYS, MONTHLY


def generate_unique_number(prefix):
    # prefix = "PAY"
    date_str = datetime.now().strftime("%Y%m%d")
    unique_str = uuid.uuid4().hex.upper()[:6]
    return f"{prefix}{date_str}{unique_str}"


def generate_ref_number(prefix, id):
    date_str = datetime.now().strftime("%Y%m%d")
    return f"{prefix}{date_str}{id}"


# calculate interest rate
# def calculate_interest_rate(principal, interest_rate, months):
#     monthly_interest_rate = interest_rate / 12 / 100
#     if monthly_interest_rate > 0:
#         payment_amount = (principal * monthly_interest_rate) / \
#             (1 - (1 + monthly_interest_rate) ** -months)
#     else:
#         payment_amount = principal / months

#     # round off to the nearest hundred
#     return int(round(payment_amount, -2))


def calculate_loan_interest_rate(loan):
    principal = loan.amount
    payment_frequency = loan.payment_frequency
    loan_term = loan.loan_term
    interest_rate = loan.interest_rate

    if payment_frequency == DAILY:
        applied_interest_rate = int(
            interest_rate / 100 * principal / MONTH_DAYS)
        payment_amount = int(principal / MONTH_DAYS) + applied_interest_rate

    elif payment_frequency == MONTHLY:
        applied_interest_rate = interest_rate / 100 * principal / loan_term
        payment_amount = int(principal / loan_term) + applied_interest_rate

    # round off to the nearest hundred
    return {'interest': int(round(applied_interest_rate, -2)), 'payment_amount': int(round(payment_amount, -2))}
