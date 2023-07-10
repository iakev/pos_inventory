"""
Module for creating serializers for Product application models
"""
from rest_framework import serializers

from administration.models import Supplier
from products.models import Category, Product, Stock, SupplierProduct

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model
    """
    class Meta:
        model = Product
        fields = ['category', 'name', 'uuid', 'code', 
                    'description', 'product_type', 'tax_type', 
                    'unit', 'limited', 'active_for_sale']

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model
    """
    class Meta:
        model = Category
        fields = ['name', 'uuid', 'image', 'thumbnail']

class StockSerializer(serializers.ModelSerializer):
    """
    Serializer for Stock model
    """
    class Meta:
        model = Stock
        fields = ['product_id', 'uuid', 'stock_quantity', 
                  'updated_at', 'cost_per_unit', 'price_per_unit_retail', 
                  'price_per_unit_wholesale', 'reorder_level', 'reorder_quantity' ]

class SupplierSerializer(serializers.ModelSerializer):
    """
    Serializer for Supplier model
    """
    class Meta:
        model = Supplier
        fields = ['uuid', 'products', 'name', 'address', 'email_address', 'phone_number']

class SupplierProductSerializer(serializers.ModelSerializer):
    """
    Serializer for SupplierProduct model
    """
    class Meta:
        model = SupplierProduct
        fields = ['supplier', 'product']
