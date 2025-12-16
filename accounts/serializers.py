from rest_framework import serializers
from .models import User, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "role")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "role")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            role=validated_data["role"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
