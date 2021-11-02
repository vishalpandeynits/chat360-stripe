import re
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

VISA_REGEX = re.compile("^4[0-9]{12}(?:[0-9]{3})?$")
MASTERCARD_REGEX = re.compile("^5[1-5][0-9]{14}$")
DISCOVER_REGEX = re.compile("^65[4-9][0-9]{13}|64[4-9][0-9]{13}|6011[0-9]{12}|(622(?:12[6-9]|1[3-9][0-9]|[2-8][0-9][0-9]|9[01][0-9]|92[0-5])[0-9]{10})$")
AMERICAN_EXPRESS_REGEX = re.compile("^3[47][0-9]{13}$")

card_regexes = {
    "visa": VISA_REGEX, 
    "mastercard": MASTERCARD_REGEX, 
    "discover": DISCOVER_REGEX, 
    "american_express": AMERICAN_EXPRESS_REGEX
}

def validate_card_expiry(value):
    if value < timezone.now().date():
        raise ValidationError(_("Expired cards not allowed"))
    return value

def card_number_validator(value):
    for regex in card_regexes.values():
        if re.search(regex, value): 
            return value
    raise ValidationError(
        _(f'{value} is not a valid card number.')
    )

def cvv_validator(value):
    if isinstance(value, int) and value > 99 and value<=999:
        return value
    if isinstance(value, str) and value.isnumeric() and int(value) > 99 and int(value)<=999:
        return int(value)
    raise ValidationError(
        _(f'{value} is an invalid CVV number.')
    )

def card_type_choice_validator(value):
    if value.lower() in {'mastercard', 'visa', 'discover', 'american_express'}:
        return value.lower()
    raise ValidationError(
        _(f'Currently we are not supporting the cards of {value} provider.')
    )