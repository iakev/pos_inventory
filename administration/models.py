"""
Module that models administration tasks for
the business
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
import uuid as uuid_lib


# Create your models here.


class Business(models.Model):
    """
    Models Administration information related to business
    """

    uuid = models.UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    tax_pin = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email_address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Owner(models.Model):
    """
    Models Business Owner information
    """

    uuid = models.UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="owners", null=True, blank=True
    )


class Employee(models.Model):
    """
    Models Employees of business
    """

    uuid = models.UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    email_address = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)


class Supplier(models.Model):
    """
    Supplier of products information
    """

    uuid = models.UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    products = models.ManyToManyField(
        "products.Product",
        related_name="suppliers",
        through="products.SupplierProduct",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255)
