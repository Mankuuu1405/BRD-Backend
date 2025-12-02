from rest_framework import serializers
from .models import (
    ChargeMaster,
    DocumentType,
    LoanProduct,
    NotificationTemplate,
    RoleMaster,
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
        fields = '__all__'
