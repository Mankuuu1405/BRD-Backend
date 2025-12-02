from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import User, UserProfile
from tenants.models import Tenant

User = get_user_model()

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

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer that handles email-based authentication.
    Accepts 'email' field in request and normalizes it to lowercase.
    """
    username_field = 'email'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Replace username field with email field in the serializer
        if 'username' in self.fields:
            self.fields['email'] = self.fields.pop('username')

    def validate(self, attrs):
        # Get email from request (accept both 'email' and 'username' keys)
        email = attrs.get('email') or attrs.get('username', '')
        email = email.lower().strip()
        
        # Map email to username field for parent serializer
        # Parent expects 'username' field but we use 'email' as USERNAME_FIELD
        attrs['username'] = email
        attrs['email'] = email  # Keep email for reference
        
        # Call parent validation
        data = super().validate(attrs)
        return data
