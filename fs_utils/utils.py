from datetime import datetime
import uuid


def generate_unique_number(prefix):
    # prefix = "PAY"
    date_str = datetime.now().strftime("%Y%m%d")
    unique_str = uuid.uuid4().hex.upper()[:6]
    return f"{prefix}{date_str}{unique_str}"


# calculate interest rate
def calculate_interest_rate(principal, interest_rate, months):
    monthly_interest_rate = interest_rate / 12 / 100
    if monthly_interest_rate > 0:
        payment_amount = (principal * monthly_interest_rate) / \
            (1 - (1 + monthly_interest_rate) ** -months)
    else:
        payment_amount = principal / months

    # round off to the nearest hundred
    return int(round(payment_amount, -2))
