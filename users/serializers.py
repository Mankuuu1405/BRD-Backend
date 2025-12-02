from rest_framework import serializers
from .models import User, UserProfile
from tenants.models import Tenant

class UserSerializer(serializers.ModelSerializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all(), required=False, allow_null=True)

    class Meta:
        model = User
        fields = ("id","email","phone","role","tenant","branch","employee_id","approval_limit","is_active","is_staff","is_superuser","created_at","updated_at")
        read_only_fields = ("created_at","updated_at")

class UserCreateSerializer(UserSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("password",)

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("id","user","tenant","role","created_at")
        read_only_fields = ("created_at",)
