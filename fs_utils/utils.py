from datetime import datetime
import uuid


def generate_unique_number(prefix):
    # prefix = "PAY"
    date_str = datetime.now().strftime("%Y%m%d")
    unique_str = uuid.uuid4().hex.upper()[:6]
    return f"{prefix}{date_str}{unique_str}"
