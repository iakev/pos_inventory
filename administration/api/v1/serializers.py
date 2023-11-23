"""
Module for serializing Administrations
"""
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from typing import Any, Dict
from rest_framework import serializers
from administration.models import Business, Employee, Owner, Supplier
from products.models import SupplierProduct
from pos_inventory.users.api.serializers import UserSerializer, UserResponseSerializer

User = get_user_model()


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
        ]


class OwnerSerializer(serializers.ModelSerializer):
    """
    Serializer for the owner model
    """

    user_uuid = serializers.UUIDField()
    business_uuid = serializers.UUIDField()

    class Meta:
        model = Owner
        fields = [
            "uuid",
            "business_uuid",
            "user_uuid",
        ]

    def validate(self, data):
        """
        Custom validation mapping user_uuid and business_uuid
        to their respective objects
        """
        user_uuid = data.pop("user_uuid", None)
        business_uuid = data.pop("business_uuid", None)
        validated_data = super().validate(data)
        if user_uuid:
            print(f"we have user_uuid as {user_uuid}")
            user = get_object_or_404(User, uuid=user_uuid)
            print(f"we have tje user object as {user}")
            validated_data["user"] = user
        if business_uuid:
            business = get_object_or_404(Business, uuid=business_uuid)
            validated_data["business"] = business
        return validated_data

    # def create(self, validated_data):
    #     """
    #     Overwriting this method to handle the owner nested creation
    #     NB: Since owner is a nested field
    #     """

    def update(self, owner, validated_data):
        """
        Updates Nested Owner data
        """
        user = validated_data.get("user", None)
        business = validated_data.get("business", None)
        if user:
            owner.user = user
        if business:
            owner.business = business
        owner.save()
        return owner

    def to_representation(self, instance):
        """
        Delegating representation to appropriate serializer
        """
        return OwnerResponseSerializer(context=self.context).to_representation(instance)


class OwnerResponseSerializer(serializers.ModelSerializer):
    """
    Custom Response data serializer for owner
    """

    user = UserResponseSerializer()
    business = BusinessSerializer(required=False)

    class Meta:
        model = Owner
        fields = ["uuid", "user", "business"]


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
            user_serializer = UserSerializer(user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user = user_serializer.update(user, user_serializer.validated_data)
                employee.user = user
            else:
                raise serializers.ValidationError(user_serializer.errors)
        employee.address = validated_data.get("address", employee.address)
        employee.department = validated_data.get("department", employee.department)
        employee.phone_number = validated_data.get("phone_number", employee.phone_number)
        employee.email_address = validated_data.get("email_address", employee.email_address)
        employee.save()
        return employee


class EmployeeRestrictedSerializer(serializers.ModelSerializer):
    """
    Custom serializer for employee serializer Response in ather viewsets
    """

    user = UserResponseSerializer()

    class Meta:
        model = Employee
        fields = ["user", "department"]


class AdministrationNotFoundSerializer(serializers.Serializer):
    detail = serializers.CharField(default="Unfortunately requested resource not found")
