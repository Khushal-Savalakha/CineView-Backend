from rest_framework import serializers
from .models import UserData
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ["name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Hash password before saving
        validated_data["password"] = make_password(validated_data.get("password"))
        return super().create(validated_data)

    def to_representation(self, instance):
        # Remove password from response
        ret = super().to_representation(instance)
        ret.pop("password", None)
        return ret
