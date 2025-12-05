from rest_framework import viewsets, permissions
from .models import Tenant, Branch
from .serializers import TenantSerializer, BranchSerializer

class IsMasterOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = getattr(request,"user",None)
        return bool(user and (getattr(user,"role",None)=="MASTER_ADMIN" or user.is_superuser))

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all().order_by('-created_at')
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated, IsMasterOrReadOnly]

    def get_queryset(self):
        user = getattr(self.request,"user",None)
        if user and (getattr(user,"role",None)=="MASTER_ADMIN" or user.is_superuser):
            return Tenant.objects.all().order_by('-created_at')
        if user and user.tenant:
            return Tenant.objects.filter(pk=user.tenant.pk)
        return Tenant.objects.none()

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all().order_by('-created_at')
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = getattr(self.request, "user", None)

        # Master admin or superuser → see everything
        if user and (getattr(user, "role", None) == "MASTER_ADMIN" or user.is_superuser):
            return Branch.objects.all()

        # Normal user → only their tenant's branches
        if user and getattr(user, "tenant", None):
            return Branch.objects.filter(tenant=user.tenant)

        return Branch.objects.none()
    

    def perform_create(self, serializer):
        user = self.request.user

        print("============ BRANCH CREATE DEBUG ============")
        print("USER:", user)
        print("USER ID:", user.id)
        print("ROLE:", getattr(user, "role", None))
        print("TENANT:", getattr(user, "tenant", None))
        print("==============================================")

        # TEMPORARY SAFE FALLBACK
        if getattr(user, "tenant", None) is None:
            raise ValueError("User has NO tenant. Cannot create branch.")

        serializer.save(tenant=user.tenant)
