from django.core.exceptions import ValidationError
from datetime import datetime
from django.core.validators import validate_email
import pytz


def is_valid_email(email):
    try:
        validate_email(email)
        print(f"Email '{email}' is valid.")
        return True
    except ValidationError:
        return False


def get_date(date, format="%Y-%m-%d %H:%M:%S"):
    date = date.astimezone(pytz.FixedOffset(300))
    return date.strftime(format)
