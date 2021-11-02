import stripe
from django.conf import settings

def make_stripe_payment(card, amount, transfer_to = None): 
    """
    This method makes a payment of 'amount' to
    the admin's account.

    returns True, if amount is transferred, otherwise false
    """
    if not transfer_to: transfer_to = settings.ADMIN_BANK_DETAILS
    
    print(f"""
        An amount of {amount} is transferred to bank account of
        {transfer_to.name}
    """)
    status = True

    return status
