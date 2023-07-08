"""
Module that contains the Models that relate to Sales
and Sales of products
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from administration.models import Business, Employee, Customer
from products.models import Product
# Create your models here.

class PaymentMode(models.Model):
    """
    Models the allowed payment Types
    """
    class PaymentMethod(models.TextChoices):
        """
        Enums for payment methods and their codes
        """
        CASH = "01", _("CASH")
        CREDIT = "02", _("CREDIT")
        CASH_CREDIT = "03", _("CASH/CREDIT")
        BANK_CHECK = "04", _("BANK CHECK")
        CARD = "05", _("DEBIT AND CREDIT CARD")
        MOBILE_MONEY = "06", _("MOBILE MONEY")
        OTHER = "07", _("OTHER")

    mode = models.CharField(max_length=3, choices=PaymentMethod.choices)
    properties = models.JSONField()

    # Logic to populate properties according to mode and then save to database


class Sales(models.Model):
    """
    Sales Model information
    """
    class TransactionProgress(models.TextChoices):
        """
        Enums for TransactionProgress values and their codes
        """
        Wait = "01", _("Wait for Approval")
        Approved = "02", _("Approved")
        Credit_Note_Request = "03", _("Credit Note Requested")
        Cancelled = "04", _("Cancelled")
        Credit_Note_Generated = "05", _("Credit Note Generated")
        Transferred = "06", _("Transferred")
    
    class SalesReceiptType(models.TextChoices):
        """
        Enums for SalesReceipt with their codes
        """
        SALE = "S", _("Sale")
        CREDIT_NOTE = "C", _("Credit Note")
    
    class TransactionType(models.Model):
        """
        Enums for the TransactionType model
        """
        COPY = "C", _("Copy")
        NORMAL = "N", _("Normal")
        PROFORMA = "P", _("Proforma")
        TRAINING = "T", _("Training")
    
    customer_id = models.ForeignKey(Customer, related_name='sales', on_delete=models.CASCADE, null= True, blank=True)
    business_id = models.OneToOneField(Business, related_name='sale', on_delete=models.CASCADE)
    payment_id = models.OneToOneField(PaymentMode, related_name='sale', on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now=True)
    time_paid = models.DateTimeField(null=True)
    sale_amount_with_tax = models.DecimalField(max_digits=10,decimal_places=2,default=0.00,blank=True)    
    tax_amount = models.DecimalField(max_digits=10, blank=True,default=0.00, decimal_places=2)
    receipt_type = models.CharField(max_length=2, choices = SalesReceiptType.choices)
    transaction_type = models.CharField(max_length=2, choices=TransactionProgress.choices)
    sale_status = models.CharField(max_length=3, choices=TransactionProgress.choices, null=True, blank=True)
    cashier_id = models.ForeignKey(Employee, related_name='sales', on_delete=models.CASCADE)
