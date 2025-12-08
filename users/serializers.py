# users/serializer.py

from rest_framework import serializers
from .models import User, AuditLog, UserProfile
from tenants.models import Tenant

class UserSerializer(serializers.ModelSerializer):
    # ✅ FIX 1: Tenant को UUID (tenant_id) से accept करें
    tenant = serializers.SlugRelatedField(
        slug_field='tenant_id', 
        queryset=Tenant.objects.all(), 
        required=False, 
        allow_null=True
    )
    
    # ✅ FIX 2: Password field जोड़ें (Write Only)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            "id", "email", "first_name", "last_name", "phone", "role", 
            "tenant", "branch", "employee_id", "approval_limit", 
            "is_active", "is_staff", "is_superuser", "created_at", "updated_at",
            "password"  # Password field list mein add kiya
        )
        read_only_fields = ("created_at", "updated_at")

    def create(self, validated_data):
        # Password को अलग निकालें और Hash करें
        password = validated_data.pop('password', None)
        
        # User create करें
        user = User.objects.create(**validated_data)
        
        # Password set करें (Hashing)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        # बाकी फील्ड्स अपडेट करें
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        # अगर पासवर्ड नया आया है तो उसे भी अपडेट करें
        if password:
            instance.set_password(password)
            
        instance.save()
        return instance

# Audit Log Serializer (इसे जैसा है वैसा ही रहने दें)
class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = AuditLog
        fields = '_all_'

# Signup Serializer (पब्लिक साइनअप के लिए)
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'role', 'phone']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'BORROWER'),
            phone=validated_data.get('phone', '')
        )
        return user