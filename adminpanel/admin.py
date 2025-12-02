from django.contrib import admin
from .models import (
    ChargeMaster,
    DocumentType,
    LoanProduct,
    NotificationTemplate,
    RoleMaster
)

@admin.register(ChargeMaster)
class ChargeMasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'charge_type', 'value', 'is_percentage', 'created_at')
    search_fields = ('name',)


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'category', 'is_required', 'created_at')
    search_fields = ('name', 'code')


@admin.register(LoanProduct)
class LoanProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'loan_type', 'min_amount', 'max_amount',
                    'interest_rate', 'processing_fee', 'created_at')
    search_fields = ('name',)


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'template_type', 'is_active', 'created_at')
    search_fields = ('name',)


@admin.register(RoleMaster)
class RoleMasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_by', 'created_at')
    search_fields = ('name',)
