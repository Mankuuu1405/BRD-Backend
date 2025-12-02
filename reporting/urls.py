from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, AnalyticsViewSet, DashboardStatsView

router = DefaultRouter()
router.register('reports', ReportViewSet, basename='report')
router.register('analytics', AnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/full', DashboardStatsView.as_view(), name='dashboard-full'),
]