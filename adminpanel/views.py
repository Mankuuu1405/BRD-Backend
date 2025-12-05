from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import (
    ChargeMaster,
    DocumentType,
    LoanProduct,
    NotificationTemplate,
    RoleMaster,
)

from .serializers import (
    ChargeMasterSerializer,
    DocumentTypeSerializer,
    LoanProductSerializer,
    NotificationTemplateSerializer,
    RoleMasterSerializer,
)

# ---------------------------
# CRUD Viewsets
# ---------------------------

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
