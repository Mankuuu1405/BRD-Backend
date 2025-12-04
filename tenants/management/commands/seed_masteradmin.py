from django.core.management.base import BaseCommand
from tenants.models import Tenant, Branch
from adminpanel.models import ChargeMaster, DocumentType, LoanProduct, RoleMaster
from users.models import User


class Command(BaseCommand):
    help = "Seed Master Admin dummy data (tenants, branches, users, and master admin models)"

    def handle(self, *args, **kwargs):

        # -----------------------------
        # 1. Create Tenant
        # -----------------------------
        tenant, created = Tenant.objects.get_or_create(
            name="Sample Finance Pvt Ltd",
            defaults={
                "email": "info@samplefinance.com",
                "phone": "9876543210",
                "address": "Hyderabad",
            },
        )
        self.stdout.write(self.style.SUCCESS(f"[TENANT] {tenant.name}"))

        # -----------------------------
        # 2. Create Branch
        # -----------------------------
        branch, created = Branch.objects.get_or_create(
            tenant=tenant,
            name="Main Branch",
            defaults={"address": "Hyderabad HO"},
        )
        self.stdout.write(self.style.SUCCESS(f"[BRANCH] {branch.name}"))

        # -----------------------------
        # 3. Create Role (RoleMaster model - adminpanel)
        # -----------------------------
        role, created = RoleMaster.objects.get_or_create(
            name="Admin",
            defaults={"description": "Primary admin role"},
        )
        self.stdout.write(self.style.SUCCESS(f"[ROLE] {role.name}"))

        # -----------------------------
        # 4. Create User (Custom User Model)
        # -----------------------------
        if not User.objects.filter(email="admin@sample.com").exists():
            user = User.objects.create(
                email="admin@sample.com",
                phone="9999999999",
                role="MASTER_ADMIN",   # Taken from ROLE_CHOICES
                tenant=tenant,
                branch=branch,
                employee_id="EMP001",
                approval_limit=500000,
                is_active=True,
                is_staff=True,
            )
            user.set_password("Admin@123")
            user.save()
            self.stdout.write(self.style.SUCCESS(f"[USER] {user.email} created"))
        else:
            self.stdout.write(self.style.WARNING("[USER] admin@sample.com already exists"))

        # -----------------------------
        # 5. Loan Products
        # -----------------------------
        lp, created = LoanProduct.objects.get_or_create(
            name="Personal Loan",
            defaults={
                "interest_rate": 12.5,
                "max_amount": 500000,
                "min_amount": 10000,
            },
        )
        self.stdout.write(self.style.SUCCESS(f"[LOAN PRODUCT] {lp.name}"))

        # -----------------------------
        # 6. Charges
        # -----------------------------
        ChargeMaster.objects.get_or_create(
            name="Processing Fee",
            charge_type="processing",
            value=300,
            is_percentage=False,
        )
        self.stdout.write(self.style.SUCCESS("[CHARGE] Processing Fee"))

        # -----------------------------
        # 7. Document Types
        # -----------------------------
        DocumentType.objects.get_or_create(
            name="Aadhaar Card",
            code="AADHAAR",
            category="KYC",
            is_required=True,
        )

        DocumentType.objects.get_or_create(
            name="PAN Card",
            code="PAN",
            category="KYC",
            is_required=True,
        )
        self.stdout.write(self.style.SUCCESS("[DOCUMENTS] Aadhaar & PAN"))

        self.stdout.write(self.style.SUCCESS("\n🎉 Seeder Completed Successfully!"))
