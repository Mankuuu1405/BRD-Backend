from rest_framework import serializers
from .models import Tenant, Branch

class BranchSerializer(serializers.ModelSerializer):
    tenant = serializers.SlugRelatedField(
        queryset=Tenant.objects.all(),
        slug_field='tenant_id'  # <-- use UUIDField
    )
 
    class Meta:
        model = Branch
        fields = "__all__"

class TenantSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, read_only=True)
    class Meta:
        model = Tenant
        fields = ("tenant_id","name","slug","tenant_type","email","phone","address","city","state","pincode","is_active","created_at","branches")
        read_only_fields = ("tenant_id","slug","created_at")
