from django.db import models
import uuid
from django.utils.text import slugify

class Tenant(models.Model):
    tenant_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    tenant_type = models.CharField(max_length=50, choices=[('BANK','Bank'),('NBFC','NBFC'),('P2P','P2P'),('FINTECH','FinTech')])
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tenants'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Branch(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='branches')
    branch_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'branches'
        verbose_name_plural = 'Branches'

    def __str__(self):
        return f"{self.name} ({self.tenant.name})"
