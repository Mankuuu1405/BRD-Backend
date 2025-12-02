from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ChargeMasterViewSet,
    DocumentTypeViewSet,
    LoanProductViewSet,
    NotificationTemplateViewSet,
    RoleMasterViewSet,
)

router = DefaultRouter()
router.register(r'charges', ChargeMasterViewSet)
router.register(r'document-types', DocumentTypeViewSet)
router.register(r'loan-products', LoanProductViewSet)
router.register(r'notification-templates', NotificationTemplateViewSet)
router.register(r'role-masters', RoleMasterViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("lead-management/", include("adminpanel.lead_management.urls")),
]
