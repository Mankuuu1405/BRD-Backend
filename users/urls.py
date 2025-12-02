from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet, signup

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    path("signup/", signup, name="user-signup"),  # Public signup endpoint
    path("", include(router.urls)),
]
