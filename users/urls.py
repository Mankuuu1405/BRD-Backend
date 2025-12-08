from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AuditLogViewSet, SignupView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'audit-logs', AuditLogViewSet)

urlpatterns = [
    # ✅ Signup Endpoint
    path('signup/', SignupView.as_view(), name='signup'),

    # Default Router URLs
    path('', include(router.urls)),
]