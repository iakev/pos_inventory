"""
Module for creating serializerd for Sales application models
"""
from rest_framework import serializers

from administration.models import Business, Employee
from administration.api.v1.serializers import BusinessSerializer, EmployeeSerializer
from sales.models import PaymentMode, ProductSales, Sales, Customer
from products.models import Product
from products.api.v1.serializers import ProductSerializer
from sales.models import Sales


class SalesSerializer(serializers.ModelSerializer):
    """
    Serializer for Sales model
    """

    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Sales
        fields = [
            "uuid",
            "customer_id",
            "business_id",
            "payment_id",
            "cashier_id",
            "products",
            "time_created",
            "sale_amount_with_tax",
            "tax_amount",
            "receipt_type",
            "transaction_type",
            "sale_status",
            "created_at",
            "updated_at",
        ]


class ProductSalesSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductSales model
    """

    products = ProductSerializer(many=True, read_only=True)
    sales = SalesSerializer(many=True, read_only=True)

    class Meta:
        model = ProductSales
        fields = [
            "uuid",
            "products",
            "sales",
            "quantity_sold",
            "price_per_unit",
            "is_wholesale",
            "price",
            "tax_amount",
            "receipt_label",
            "tax_rate",
            "business_name",
            "business_pin",
            "address",
            "created_at",
            "updated_at",
        ]


class PaymentModeSerializer(serializers.Serializer):
    """
    Serializer for PaymentMode model
    """

    class Meta:
        model = PaymentMode
        fileds = ["uuid", "mode", "properties"]


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model"""

    class Meta:
        model = Customer
        fields = [
            "uuid",
            "created_at",
            "updated_at",
            "name",
            "address",
            "tax_pin",
            "email_address",
        ]
