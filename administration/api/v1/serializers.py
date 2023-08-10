"""
Module for serializing Administrations
"""
from django.contrib.auth import get_user_model
from typing import Any
from rest_framework import serializers
from administration.models import Business, Employee
from pos_inventory.users.api.serializers import UserSerializer

User = get_user_model()


class BusinessSerializer(serializers.ModelSerializer):
    """Serializer for Business model"""

    owner = UserSerializer(required=False)  # fro partial update

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

    def create(self, validated_data):
        """
        Overwriting this method inorder to deal with
        the nested User instance creation
        """
        owner_data = validated_data.pop("owner")
        owner_serializer = UserSerializer(data=owner_data)
        if owner_serializer.is_valid():
            owner = owner_serializer.save()
            validated_data["owner"] = owner
            return super().create(validated_data)
        raise serializers.ValidationError(owner_serializer.errors)

    def update(self, business, validated_data):
        """
        Nested fields update method not handled by default
        We never update the user instance except when we need to then we are creating
        a new user
        """
        owner_data = validated_data.pop("owner", None)
        if owner_data:
            owner = business.owner
            owner_serializer = UserSerializer(data=owner_data)
            if owner_serializer.is_valid():
                owner = owner_serializer.update(owner, owner_serializer.validated_data)
                business.owner = owner
            else:
                raise serializers.ValidationError(owner_serializer.errors)
        business.name = validated_data.get("name", business.name)
        business.address = validated_data.get("address", business.address)
        business.tax_pin = validated_data.get("tax_pin", business.tax_pin)
        business.phone_number = validated_data.get(
            "phone_number", business.phone_number
        )
        business.email_address = validated_data.get(
            "email_address", business.email_address
        )
        business.save()
        return business


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee model"""

    user = UserSerializer(required=False)  # for partial updatte

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

    def create(self, validated_data):
        """
        Overwriting this method inorder to deal with
        the nested User instance creation
        """
        user_data = validated_data.pop("user")
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            validated_data["user"] = user
            return super().create(validated_data)
        raise serializers.ValidationError(user_serializer.errors)

    def update(self, employee, validated_data):
        """
        Nested fields update method not handled by default
        We never update the user instance except when we need to then we are creating
        a new user
        """
        user_data = validated_data.pop("user", None)
        if user_data:
            user = employee.user
            print(f"we have the user as {user}")
            user_serializer = UserSerializer(user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user = user_serializer.update(user, user_serializer.validated_data)
                employee.user = user
            else:
                raise serializers.ValidationError(user_serializer.errors)
        employee.address = validated_data.get("address", employee.address)
        employee.department = validated_data.get("department", employee.department)
        employee.phone_number = validated_data.get(
            "phone_number", employee.phone_number
        )
        employee.email_address = validated_data.get(
            "email_address", employee.email_address
        )
        employee.save()
        return employee
