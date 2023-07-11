"""
Module for serializing Administrations
"""
from rest_framework import serializers
from administration.models import Business, Customer, Employee


class BusinessSerializer(serializers.ModelSerializer):
    """Serializer for Business model"""

    class Meta:
        model = Business
        fields = [
            "uuid",
            "created_at",
            "updated_at",
            "name",
            "address",
            "tax_pin",
            "phone_number",
            "email_address",
            "owner",
        ]


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model"""

    class Meta:
        model = Customer
        fields = ["uuid", "created_at", "updated_at", "name", "address", "tax_pin", "email_address"]


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee model"""

    class Meta:
        model = Employee
        fields = [
            "uuid",
            "created_at",
            "updated_at",
            "user",
            "phone_number",
            "address",
            "department",
        ]
