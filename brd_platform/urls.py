from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import home

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),

    # Authentication
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # App URLs
    path("api/v1/tenants/", include("tenants.urls")),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/crm/", include("crm.urls")),
    path("api/v1/integrations/", include("integrations.urls")),
    
    # 👇 ये नए URLs जोड़ें ताकि Adminpanel, Communications, आदि काम करें
    path("api/v1/adminpanel/", include("adminpanel.urls")),
    path("api/v1/communications/", include("communications.urls")),
    # path("api/v1/los/", include("los.urls")), # इसे तब uncomment करें जब los/urls.py बन जाए
    # path("api/v1/lms/", include("lms.urls")), # इसे तब uncomment करें जब lms/urls.py बन जाए
    
    path("api/v1/", include("reporting.urls")), 
]