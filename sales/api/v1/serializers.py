"""
Module for creating serializerd for Sales application models
"""
from typing import Any
from rest_framework import serializers

from administration.models import Business, Employee
from administration.api.v1.serializers import BusinessSerializer, EmployeeSerializer
from sales.models import PaymentMode, ProductSales, Sales, Customer
from products.models import Product
from products.api.v1.serializers import ProductSerializer


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


class PaymentModeSerializer(serializers.ModelSerializer):
    """
    Serializer for PaymentMode model
    """

    properties = serializers.JSONField(required=False)

    class Meta:
        model = PaymentMode
        fields = ["uuid", "payment_method", "properties"]

    def create(self, validated_data):
        """Create a new payment mode"""
        properties = validated_data.pop(
            "properties", {}
        )  # Get the properties data or an empty dictionary if not provided
        payment_mode = PaymentMode(**validated_data)
        payment_mode.properties = properties
        payment_mode.save()
        return payment_mode

    def update(self, payment, validated_data):
        """Update a payment mode instance"""
        properties_data = validated_data.pop(
            "properties", None
        )  # Get the properties data or an empty dictionary if not provided
        if properties_data:
            payment.properties = properties_data
        payment.mode = validated_data.get("mode", payment.mode)
        payment.save()
        return payment


class SalesSerializer(serializers.ModelSerializer):
    """
    Serializer for Sales model
    """

    products = ProductSerializer(many=True, read_only=True)
    business_id = BusinessSerializer(read_only=True)
    cashier_id = EmployeeSerializer(read_only=True)
    payment_id = PaymentModeSerializer(read_only=True)
    customer_id = CustomerSerializer(read_only=True)

    class Meta:
        model = Sales
        fields = [
            "uuid",
            "customer_id",
            "business_id",
            "payment_id",
            "cashier_id",
            "products",
            "sale_amount_with_tax",
            "tax_amount",
            "receipt_type",
            "transaction_type",
            "receipt_label",
            "sale_status",
            "created_at",
            "updated_at",
        ]


class ProductSalesRelatedSaleSerializer(serializers.ModelSerializer):
    """
    Serializer for related Sale model within ProductSales
    """

    # Customize the fields you want to include for the related Sale model
    class Meta:
        model = Sales
        fields = ["uuid", "created_at", "updated_at", "sale_status"]


class ProductSalesSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductSales model
    """

    product = ProductSerializer(read_only=True)
    sale = ProductSalesRelatedSaleSerializer(read_only=True)

    class Meta:
        model = ProductSales
        fields = [
            "uuid",
            "product",
            "sale",
            "quantity_sold",
            "price_per_unit",
            "is_wholesale",
            "price",
            "tax_amount",
            "tax_rate",
            "created_at",
            "updated_at",
        ]
