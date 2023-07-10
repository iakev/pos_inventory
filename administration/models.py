"""
Module that models administration tasks for
the business
"""
from django.conf import settings
from django.db import models
import uuid as uuid_lib

# Create your models here.
class Business(models.Model):
    """
    Models Administration information related to business
    """
    uuid = models.UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    tax_pin = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email_address = models.CharField(max_length=255, null=True, blank=True)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Employee(models.Model):
    """
    Models Employees of business
    """
    uuid = models.UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)

class Customer(models.Model):
    """
    Models the product buyer information all optional
    """
    uuid = models.UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    tax_pin = models.CharField(max_length=255, null=True, blank=True)
    email_address = models.CharField(max_length=255, null=True, blank=True)

class Supplier(models.Model):
    """
    Supplier of products information
    """
    uuid = models.UUIDField(editable=False, db_index=True, default=uuid_lib.uuid4)
    products = models.ManyToManyField("products.Product", related_name="suppliers", through="products.SupplierProduct")
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255)
