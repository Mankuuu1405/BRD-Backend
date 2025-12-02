from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth

# Import Local Models
from .models import Report, Analytics
from .serializers import ReportSerializer, AnalyticsSerializer
from users.permissions import DefaultPermission
from tenants.models import Tenant
from users.models import User
from los.models import LoanApplication
from crm.models import LeadActivity

# --- EXISTING VIEWSETS (Do not remove) ---

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [DefaultPermission]

class AnalyticsViewSet(viewsets.ModelViewSet):
    queryset = Analytics.objects.all()
    serializer_class = AnalyticsSerializer
    permission_classes = [DefaultPermission]

# --- NEW DASHBOARD API ---

class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 1. Fetch KPIs
        total_tenants = Tenant.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        total_loans = LoanApplication.objects.count()
        
        disbursed_agg = LoanApplication.objects.filter(status='DISBURSED').aggregate(Sum('amount'))
        disbursed_amount = disbursed_agg['amount__sum'] or 0
        disbursed_display = f"₹{disbursed_amount:,.0f}"

        # 2. Loan Status Distribution
        status_counts = LoanApplication.objects.values('status').annotate(count=Count('id'))
        pie_data = [{"status": item['status'], "count": item['count']} for item in status_counts]

        # 3. Monthly Disbursement
        monthly_data = (
            LoanApplication.objects.filter(status='DISBURSED')
            .annotate(month=TruncMonth('updated_at'))
            .values('month')
            .annotate(amount=Sum('amount'))
            .order_by('month')
        )
        line_chart_data = [
            {"month": m['month'].strftime('%b'), "amount": m['amount']} 
            for m in monthly_data
        ]

        # 4. Recent Activity
        recent_activities = LeadActivity.objects.select_related('lead').order_by('-created_at')[:5]
        activity_feed = [
            {
                "title": action.action,
                "subtitle": action.lead.name if action.lead else "System",
                "time": action.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for action in recent_activities
        ]

        data = {
            "kpis": {
                "totalTenants": total_tenants,
                "tenantsTrend": "+0%",
                "activeUsers": active_users,
                "usersTrend": "+0%",
                "totalLoans": total_loans,
                "loansTrend": "+0%",
                "disbursedAmount": disbursed_display,
                "amountTrend": "+0%"
            },
            "charts": {
                "monthlyDisbursement": line_chart_data,
                "loanStatusDistribution": pie_data,
                "recentActivity": activity_feed
            }
        }

        return Response(data)