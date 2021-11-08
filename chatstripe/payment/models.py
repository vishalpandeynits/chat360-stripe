import re
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .utils import encrypt, decrypt
from .validators import validate_card_expiry, card_number_validator, cvv_validator, card_type_choice_validator, card_regexes

class CardDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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

    # initially false, true when card verified by making a payment of 
    # 1 Rupeee(100 Paise)
    is_verified = models.BooleanField(default = False)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    
    def save(self, *args, **kwargs):
        self.card_number = encrypt(self.card_number)
        """
            # TODO
            1. Schedule a task to 24th hour, that if this instance is not 
            verified, delete this instance.
            2. Encrypt the card details, not required though (In custom save method or use pre_save signal)
            3. Define a custom manager/ method to retrive that card details
            after decryption(if card detail is encrypted.).
        """
        super().save(*args, **kwargs)

    @property
    def card_number_plain(self):
        return decrypt(self.card_number)

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
    #meta = jsonfield.JSONField(default = dict)

    class Meta:
        ordering = ['-transaction_datetime']
        unique_together = ('order_id', 'transaction_id',)
        verbose_name = 'Payment Detail'
        verbose_name_plural = 'Payment Details'