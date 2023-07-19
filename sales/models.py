"""
Module that contains the Models that relate to Sales
and Sales of products
"""
import uuid as uuid_lib
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from administration.models import Business, Employee
from products.models import Product, Supplier, Stock

# Create your models here.


class Customer(models.Model):
    """
    Models the product buyer information all optional
    """

    uuid = models.UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    tax_pin = models.CharField(max_length=255, null=True, blank=True)
    email_address = models.CharField(max_length=255, null=True, blank=True)


class PaymentMode(models.Model):
    """
    Models the allowed payment types
    """

    class PaymentMethod(models.TextChoices):
        CASH = "01", _("CASH")
        CREDIT = "02", _("CREDIT")
        CASH_CREDIT = "03", _("CASH/CREDIT")
        BANK_CHECK = "04", _("BANK CHECK")
        CARD = "05", _("DEBIT AND CREDIT CARD")
        MOBILE_MONEY = "06", _("MOBILE MONEY")
        OTHER = "07", _("OTHER")

    uuid = models.UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    payment_method = models.CharField(
        max_length=2, choices=PaymentMethod.choices, default=PaymentMethod.CASH
    )
    properties = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = _("Payment Mode")

    def __str__(self):
        return str(self.payment_method)

    def __str__(self):
        payment_method_labels = {
            self.PaymentMethod.CASH: "CASH",
            self.PaymentMethod.CREDIT: "CREDIT",
            self.PaymentMethod.CASH_CREDIT: "CASH/CREDIT",
            self.PaymentMethod.BANK_CHECK: "BANK CHECK",
            self.PaymentMethod.CARD: "DEBIT AND CREDIT CARD",
            self.PaymentMethod.MOBILE_MONEY: "MOBILE MONEY",
            self.PaymentMethod.OTHER: "OTHER",
        }
        return payment_method_labels.get(self.payment_method, "")


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

    class TransactionType(models.TextChoices):
        """
        Enums for the TransactionType model
        """

        COPY = "C", _("Copy")
        NORMAL = "N", _("Normal")
        PROFORMA = "P", _("Proforma")
        TRAINING = "T", _("Training")

    uuid = models.UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    customer_id = models.ForeignKey(
        Customer, related_name="sales", on_delete=models.CASCADE, null=True, blank=True
    )
    business_id = models.OneToOneField(
        Business, related_name="sale", on_delete=models.CASCADE, null=True, blank=True
    )
    payment_id = models.ForeignKey(
        PaymentMode,
        related_name="sales",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    cashier_id = models.ForeignKey(
        Employee, related_name="sales", on_delete=models.CASCADE, null=True, blank=True
    )
    products = models.ManyToManyField(
        Product, related_name="sales", through="ProductSales"
    )
    sale_amount_with_tax = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    tax_amount = models.DecimalField(
        max_digits=10, blank=True, default=0.00, decimal_places=2
    )
    receipt_type = models.CharField(max_length=2, choices=SalesReceiptType.choices)
    transaction_type = models.CharField(max_length=2, choices=TransactionType.choices)
    sale_status = models.CharField(
        max_length=3, choices=TransactionProgress.choices, null=True, blank=True
    )
    receipt_label = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "sales"
        ordering = ["created_at", "updated_at"]

    def get_absolute_url(self):
        return f"/sales/{self.uuid}"

    def __str__(self):
        return f"{self.uuid}"


class ProductSales(models.Model):
    """
    Models the through Table of Product to Sales many to many
    """

    uuid = models.UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    product = models.ForeignKey(
        Product, related_name="product_sales", on_delete=models.CASCADE
    )
    sale = models.ForeignKey(
        Sales, related_name="product_sales", on_delete=models.CASCADE
    )
    quantity_sold = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_wholesale = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_rate = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # logic for populating price_per_unit according to is_wholesale

class Purchase(models.Model):
    """Model with purchase information"""
    uuid = models.UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    user_id = models.ForeignKey(Employee, related_name="purchases", on_delete=models.CASCADE, null=True, blank=True)
    supplier_id = models.OneToOneField(Supplier, related_name="purchases", on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.ForeignKey(Stock, related_name="purchases", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    purchase_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    description = models.TextField(blank=True, null=True)