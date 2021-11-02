import re
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .stripe_payment import make_stripe_payment
from .validators import validate_card_expiry, card_number_validator, cvv_validator, card_type_choice_validator, card_regexes

class CardDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    card_number = models.CharField(max_length = 16, validators = [card_number_validator])
    card_type_choices = (
        ('mastercard', _('mastercard')),
        ('visa', _('visa')),
        ('american_express', _('American Express')),
        ('discover', _('Discover'))
    )
    card_type = models.CharField(max_length = 30, choices=card_type_choices, validators = [card_type_choice_validator], blank = True)
    expiry_date = models.DateField(validators=[validate_card_expiry])
    cvv = models.PositiveIntegerField(validators=[cvv_validator])

    # will also hold an aggregrate field called status,
    # true if date < today's date else false

    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    
    def save(self, *args, **kwargs):
        """
            1. Initiate a payment on every update/save method being called.
            Save the card details iff a valid transaction is made using this
            card.
        """
        # make a payment of 1 Rupee
        status = make_stripe_payment(card = self, amount = 1)

        #TODO --> Change print statement into logger
        if status:
            print("Payment successful, save the card credentials")
        else:
            print("Payment failed, don't save the card credentials.") 
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.username} {self.card_type} card"

    class Meta:
        ordering = ['-created_on']

@receiver(pre_save, sender = CardDetail)
def card_type_from_card_number(sender, instance, *args, **kwargs):
    card_number = instance.card_number
    for regex in card_regexes:
        if re.search(card_regexes[regex], card_number):
            card_type = regex
            break
    if card_type not in card_regexes.keys():
        card_type = 'invalid'
    instance.card_type = card_type

class Payment(models.Model):
    client = models.ForeignKey(User, on_delete = models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2, null=True)

    order_id = models.CharField(_('order_id'), max_length=50)
    transaction_id = models.CharField(max_length = 100, unique = True)

    # true , if transaction is valid, else false
    status = models.BooleanField(default = False)

    transaction_datetime = models.DateTimeField(auto_now = True)
    #meta = models.JSONField(default = dict)

    class Meta:
        ordering = ['-transaction_datetime']
        unique_together = ('order_id', 'transaction_id',)
        verbose_name = 'Payment Detail'
        verbose_name_plural = 'Payment Details'
    

