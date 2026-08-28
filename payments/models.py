from django.db import models

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Merchant(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        BLOCKED = "blocked", "Blocked"

    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    merchant_id = models.ForeignKey(
        Merchant,
        on_delete=models.PROTECT,
        related_name="projects",
    )
    project_name = models.CharField(max_length=255)
    api_key_digest = models.CharField(max_length=128, unique=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Invoice(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        UNDERPAID = "underpaid", "Underpaid"
        OVERPAID = "overpaid", "Overpaid"
        EXPIRED = "expired", "Expired"
        CANCELLED = "cancelled", "Cancelled"

    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name="invoices",
    )
    merchant_invoice_id = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    currency = models.CharField(max_length=3)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    # expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["project", "merchant_invoice_id"],
    #             name="unique_invoice_per_project",
    #         ),
    #         models.CheckConstraint(
    #             condition=models.Q(amount__gt=0),
    #             name="invoice_amount_positive",
    #         ),
    #     ]
    #     indexes = [
    #         models.Index(fields=["project", "status"]),
    #         models.Index(fields=["expires_at", "status"]),
    #     ]

    def __str__(self) -> str:
        return self.merchant_invoice_id
