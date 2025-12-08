from rest_framework import viewsets, permissions, filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny 
from rest_framework.decorators import authentication_classes, permission_classes # Optional imports

from .models import User, AuditLog
from .serializers import UserSerializer, AuditLogSerializer, UserSignupSerializer

# --- 1. User ViewSet (Protected) ---
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# --- 2. Audit Log ViewSet (Protected) ---
class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.select_related('user').all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['action_type', 'user', 'module']
    search_fields = ['description', 'user__email', 'ip_address']

# --- 3. Signup View (Public) ---
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny] 
    authentication_classes = [] # ✅ Ye line add karo: Token check disable karega