from rest_framework import serializers
from .models import (
    ChargeMaster,
    DocumentType,
    LoanProduct,
    NotificationTemplate,
    RoleMaster,
    Subscription,
    Coupon,
    Subscriber,
    EmploymentType,
    OccupationType,
)

# ---------------------------
# Charge Master Serializer
# ---------------------------
class ChargeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeMaster
        fields = '__all__'


# ---------------------------
# Document Type Serializer
# ---------------------------
class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'


# ---------------------------
# Loan Product Serializer
# ---------------------------
class LoanProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanProduct
        fields = '__all__'


# ---------------------------
# Notification Template Serializer
# ---------------------------
class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = '__all__'


# ---------------------------
# Role Master Serializer
# ---------------------------
class RoleMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleMaster
        # ✅ 'permissions' field add kiya
        fields = ['id', 'name', 'description', 'permissions', 'parent_role', 'created_by', 'created_at']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"

class CouponSerializer(serializers.ModelSerializer):
    # Accept list of UUIDs for M2M
    subscription_id = serializers.PrimaryKeyRelatedField(
        queryset=Subscription.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Coupon
        fields = "__all__"

    # Save M2M manually
    def create(self, validated_data):
        subs = validated_data.pop("subscription_id", [])
        coupon = Coupon.objects.create(**validated_data)
        coupon.subscription_id.set(subs)
        return coupon

    def update(self, instance, validated_data):
        subs = validated_data.pop("subscription_id", [])
        coupon = super().update(instance, validated_data)
        coupon.subscription_id.set(subs)
        return coupon 
    




class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'

class EmploymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentType
        fields = "__all__"


class OccupationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccupationType
        fields = "__all__"