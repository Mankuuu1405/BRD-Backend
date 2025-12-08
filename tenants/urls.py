from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import TenantViewSet, BranchViewSet

router = DefaultRouter()
router.register(r'branches', BranchViewSet, basename='branches')  # FIRST
router.register(r'', TenantViewSet, basename='tenants')            # SECOND


urlpatterns = [
    path("", include(router.urls)),
    path("onboarding/", include("tenants.client_onboarding.urls")),
]
