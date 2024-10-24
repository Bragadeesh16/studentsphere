from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if not value.isdigit():
        raise ValidationError(
            f"{value} is not a valid phone number. Only digits are allowed."
        )
    if len(value) == 10:
        raise ValidationError(f"Phone number must be at least 10 digits long.")
