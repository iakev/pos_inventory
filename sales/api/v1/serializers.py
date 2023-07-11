"""
Module for creating serializerd for Sales application models
"""
from rest_framework import serializers

from administration.models import Business, Customer, Employee
from sales.models import PaymentMode, ProductSales, Sales
from products.models import Product


class SalesSerializer(serializers.Serializer):
    """
    Serializer for Sales model
    """

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
            "sale_status" "created_at",
            "updated_at",
        ]


class ProductSalesSerializer(serializers.Serializer):
    """
    Serializer for ProductSales model
    """

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
