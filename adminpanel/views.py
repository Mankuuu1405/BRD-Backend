from rest_framework import viewsets, status
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



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
    OccupationType
)

from .serializers import (
    ChargeMasterSerializer,
    DocumentTypeSerializer,
    LoanProductSerializer,
    NotificationTemplateSerializer,
    RoleMasterSerializer,
    SubscriptionSerializer,
    CouponSerializer,
    SubscriberSerializer,
    EmploymentTypeSerializer,
    OccupationTypeSerializer
)

class ChargeMasterViewSet(viewsets.ModelViewSet):
    queryset = ChargeMaster.objects.all()
    serializer_class = ChargeMasterSerializer
    permission_classes = [IsAuthenticated]

class DocumentTypeViewSet(viewsets.ModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    permission_classes = [IsAuthenticated]

class LoanProductViewSet(viewsets.ModelViewSet):
    queryset = LoanProduct.objects.all()
    serializer_class = LoanProductSerializer
    permission_classes = [IsAuthenticated]

class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAuthenticated]

class RoleMasterViewSet(viewsets.ModelViewSet):
    queryset = RoleMaster.objects.all()
    serializer_class = RoleMasterSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get', 'post'], url_path='permissions')
    def handle_permissions(self, request, pk=None):
        role = self.get_object()

        if request.method == 'GET':
            return Response(role.permissions or {})

        elif request.method == 'POST':
            new_perms = request.data.get('permissions', {})
            role.permissions = new_perms
            role.save()
            return Response(role.permissions, status=status.HTTP_200_OK)
        
class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.filter(isDeleted=False)
    serializer_class = SubscriptionSerializer
    lookup_field = "uuid"  

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.filter(isDeleted=False)
    serializer_class = CouponSerializer
    lookup_field = "uuid"   # IMPORTANT


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.filter(isDeleted=False)
    serializer_class = SubscriberSerializer
    lookup_field = "uuid"

    def destroy(self, request, *args, **kwargs):
        """Soft Delete Instead of Hard Delete"""
        instance = self.get_object()
        instance.isDeleted = True
        instance.modified_user = request.user.username or "System"
        instance.save()
        return Response(
            {"message": "Subscriber soft-deleted successfully"},
            status=status.HTTP_200_OK
        )

    def perform_create(self, serializer):
        """Save created_user automatically"""
        serializer.save(
            created_user=self.request.user.username or "System"
        )

    def perform_update(self, serializer):
        """Save modified_user automatically"""
        serializer.save(
            modified_user=self.request.user.username or "System"
        )

    
class EmploymentTypeViewSet(viewsets.ModelViewSet):
    queryset = EmploymentType.objects.filter(isDeleted=False)
    serializer_class = EmploymentTypeSerializer
    lookup_field = "uuid"

    # Safe username method
    def get_username(self):
        user = self.request.user
        return (
            getattr(user, "username", None)
            or getattr(user, "email", None)
            or getattr(user, "phone", None)
            or "System"
        )

    def perform_create(self, serializer):
        serializer.save(created_user=self.get_username())

    def perform_update(self, serializer):
        serializer.save(modified_user=self.get_username())

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.isDeleted = True
        instance.modified_user = self.get_username()
        instance.save()
        return Response({"message": "Employment type soft-deleted successfully"}, status=200)


class OccupationTypeViewSet(viewsets.ModelViewSet):
    queryset = OccupationType.objects.filter(isDeleted=False)
    serializer_class = OccupationTypeSerializer
    lookup_field = "uuid"

    def get_username(self):
        user = self.request.user
        return (
            getattr(user, "username", None)
            or getattr(user, "email", None)
            or getattr(user, "phone", None)
            or "System"
        )

    def perform_create(self, serializer):
        serializer.save(created_user=self.get_username())

    def perform_update(self, serializer):
        serializer.save(modified_user=self.get_username())

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.isDeleted = True
        instance.modified_user = self.get_username()
        instance.save()
        return Response({"message": "Occupation type soft-deleted successfully"}, status=200)
       

    