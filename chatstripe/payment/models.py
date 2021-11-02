from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.

class CardDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    card_number = models.CharField(max_length = 16)
    card_type = (
        ('mastercard', _('mastercard')),
        ('visa', _('visa')),
        ('american_express', _('American Express')),
        ('discover', _('Discover'))
    )
    card_type = models.CharField(max_length = 30)
    expiry_date = models.DateField()
    
    # will also hold an aggregrate field called status,
    # true if date < today's date else false

    action = models.CharField(max_length = 30)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    
    """
        TODO
        Add these validators.
        1. Card number validator.
        2. Card type must be one of the mentioned card types.
        3. expired_card must not be added.
        4. Initiate a payment after every update on or save method.
    """

    def save(self, *args, **kwargs):
        # TODO
        """
            1. Save the card details iff a valid transaction is made using this
            card.
        """
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.username} {self.card_type} card"

    class Meta:
        ordering = ['-created_on']

class Payment(models.Model):
    client = models.ForeignKey(User, on_delete = models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2, null=True)

    order_id = models.CharField(_('order_id'), max_length=50)
    transaction_id = models.CharField(max_length = 100, unique = True)

    # true , if transaction is valid, else false
    status = models.BooleanField()

    transaction_datetime = models.DateTimeField(auto_now = True)
    #meta = models.JSONField(default = dict)

    class Meta:
        ordering = ['-transaction_datetime']
        unique_together = ('order_id', 'transaction_id',)
        verbose_name = 'Payment Detail'
        verbose_name_plural = 'Payment Details'
    

