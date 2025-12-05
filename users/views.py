from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, UserCreateSerializer

class IsTenantAdminOrMaster(permissions.BasePermission):
    """
    Custom permission: Only allow tenant admins to manage their own users.
    Master admins can manage everyone.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Master Admin can access everything
        if request.user.is_superuser or getattr(request.user, "role", None) == "MASTER_ADMIN":
            return True
        # Tenant Admin can only access users within their own tenant
        return obj.tenant == request.user.tenant

class UserViewSet(viewsets.ModelViewSet):
    # Default queryset (will be filtered in get_queryset)
    queryset = User.objects.all().order_by('-created_at')
    permission_classes = [permissions.IsAuthenticated, IsTenantAdminOrMaster]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        """
        Filter users so tenant admins only see their own users.
        """
        user = getattr(self.request, "user", None)
        
        # If user is not authenticated properly, return empty
        if not user or not user.is_authenticated:
            return User.objects.none()

        # 1. Master Admin / Superuser sees EVERYTHING
        if getattr(user, "role", None) == "MASTER_ADMIN" or user.is_superuser:
            return User.objects.all().order_by('-created_at')

        # 2. Tenant Admin sees only users in THEIR Tenant
        if user.tenant:
            return User.objects.filter(tenant=user.tenant).order_by('-created_at')

        # 3. If user has no tenant assigned (unlikely but possible), return nothing or self
        return User.objects.filter(id=user.id)

    def perform_create(self, serializer):
        """
        Automatically assign the current user's tenant to the new user.
        Prevent assigning a different tenant unless you are Master Admin.
        """
        user = self.request.user
        if getattr(user, "role", None) == "MASTER_ADMIN" or user.is_superuser:
            # Master admin can specify tenant in the serializer data
            serializer.save()
        else:
            # Force the new user to be in the admin's tenant
            serializer.save(tenant=user.tenant)

    def perform_update(self, serializer):
        """
        Ensure tenant field cannot be changed by tenant admins.
        """
        user = self.request.user
        if getattr(user, "role", None) != "MASTER_ADMIN" and not user.is_superuser:
            # If not master admin, ignore any 'tenant' field passed in update
            # This prevents moving a user to another tenant
            serializer.save(tenant=user.tenant)
        else:
            serializer.save()

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Return the currently logged-in user's profile.
        """
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)