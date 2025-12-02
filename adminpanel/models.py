from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# ---------------------------
# 1. Charge Master
# ---------------------------
class ChargeMaster(models.Model):
    CHARGE_TYPES = (
        ('processing', 'Processing Fee'),
        ('penalty', 'Penalty'),
        ('other', 'Other Charges'),
    )

    name = models.CharField(max_length=200)
    charge_type = models.CharField(max_length=20, choices=CHARGE_TYPES)
    is_percentage = models.BooleanField(default=False)
    value = models.DecimalField(max_digits=10, decimal_places=2)   # NOTE: field name = value
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "admin_charge_master"

    def __str__(self):
        return f"{self.name} ({self.charge_type})"


# ---------------------------
# 2. Document Types
# ---------------------------
class DocumentType(models.Model):
    CATEGORY_TYPES = (
        ('kyc', 'KYC Document'),
        ('income', 'Income Document'),
        ('other', 'Other'),
    )

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_TYPES, default='other')
    description = models.TextField(null=True, blank=True)
    is_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "admin_document_types"

    def __str__(self):
        return self.name


# ---------------------------
# 3. Loan Products
# ---------------------------
class LoanProduct(models.Model):
    LOAN_TYPES = (
        ('personal', 'Personal Loan'),
        ('car', 'Car Loan'),
        ('home', 'Home Loan'),
        ('business', 'Business Loan'),
    )

    name = models.CharField(max_length=200)
    loan_type = models.CharField(max_length=50, choices=LOAN_TYPES)
    description = models.TextField(null=True, blank=True)

    min_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    processing_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    min_tenure_months = models.IntegerField(default=1)
    max_tenure_months = models.IntegerField(default=60)

    charges = models.ManyToManyField("ChargeMaster", blank=True)
    required_documents = models.ManyToManyField("DocumentType", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "admin_loan_products"

    def __str__(self):
        return self.name


# ---------------------------
# 4. Notification Templates
# ---------------------------
class NotificationTemplate(models.Model):
    TEMPLATE_TYPES = (
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('system', 'System Notification'),
    )

    name = models.CharField(max_length=200)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)
    subject = models.CharField(max_length=300, null=True, blank=True)
    body = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "admin_notification_templates"

    def __str__(self):
        return f"{self.name} ({self.template_type})"


# ---------------------------
# 5. Role Master
# ---------------------------
class RoleMaster(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(null=True, blank=True)

    parent_role = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sub_roles",
    )

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "admin_role_master"

    def __str__(self):
        return self.name
