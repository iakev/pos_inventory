from typing import Any
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["uuid", "username", "password", "first_name", "last_name"]
        extra_kwargs = {
            "username": {"required": True},
        }

    def create(self, validated_data):
        """
        create a user instance
        """
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, user, validated_data):
        """
        Updates a user instace
        """
        username = validated_data.get("username")
        if "username" in validated_data:
            username = validated_data["username"]
            if User.objects.filter(username=username).exclude(pk=user.id).exists():
                raise serializers.ValidationError("User with this username already exists.")
            user.username = username
        user.first_name = validated_data.get("first_name", user.first_name)
        user.last_name = validated_data.get("last_name", user.last_name)
        user.set_password(validated_data.get("password"), user.password)
        user.save()
        return user

    def to_representation(self, instance):
        """
        Delegating response to appropriate serializer
        """
        return UserResponseSerializer(context=self.context).to_representation(instance)


class UserResponseSerializer(serializers.ModelSerializer):
    """
    Response Serializer for User data
    """

    class Meta:
        model = User
        fields = ["uuid", "username", "first_name", "last_name"]


class UserResponseSerializerAvecNameSole(serializers.ModelSerializer):
    """
    Response Serializer for user data with only first_name and last_name
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name"]
