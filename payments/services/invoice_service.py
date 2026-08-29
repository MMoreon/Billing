from datetime import datetime
from decimal import Decimal

from django.db import IntegrityError, transaction
from django.utils import timezone

from payments.models import Invoice, Project
from payments.services.exceptions import ConflictServiceError, ForbiddenServiceError, ValidationServiceError

def normalize_currency(currency: str) -> str:
    currency = currency.strip().upper()

    if len(currency) != 3 or not currency.isalpha():
        raise ValidationServiceError(
            "Currency must be a 3-letter code"
        )

    return currency

@transaction.atomic
def create_invoice(
    *,
    project: Project,
    amount: Decimal,
    currency: str,
    merchant_invoice_id: str,
    expires_at: datetime,
) -> tuple[Invoice, bool]:
    if project.merchant.status != project.merchant.Status.ACTIVE:
        raise ForbiddenServiceError("Merchant is blocked")

    merchant_invoice_id = merchant_invoice_id.strip()

    if not merchant_invoice_id:
        raise ValidationServiceError(
            "merchant_invoice_id is required"
        )

    if amount <= Decimal("0"):
        raise ValidationServiceError(
            "amount must be greater than zero"
        )

    if expires_at <= timezone.now():
        raise ValidationServiceError(
            "expires_at must be in the future"
        )

    currency = normalize_currency(currency)

    existing_invoice = (
        Invoice.objects
        .filter(
            project=project,
            merchant_invoice_id=merchant_invoice_id,
        )
        .first()
    )

    if existing_invoice is not None:
        same_data = (
            existing_invoice.amount == amount
            and existing_invoice.currency == currency
            and existing_invoice.expires_at == expires_at
        )

        if not same_data:
            raise ConflictServiceError(
                "Invoice with this merchant_invoice_id "
                "already exists with different data"
            )

        return existing_invoice, False

    try:
        invoice = Invoice.objects.create(
            project=project,
            amount=amount,
            currency=currency,
            merchant_invoice_id=merchant_invoice_id,
            expires_at=expires_at,
        )
    except IntegrityError:
# защита от гонки двух запросов
        invoice = Invoice.objects.get(
            project=project,
            merchant_invoice_id=merchant_invoice_id,
        )

        same_data = (
            invoice.amount == amount
            and invoice.currency == currency
            and invoice.expires_at == expires_at
        )

        if not same_data:
            raise ConflictServiceError(
                "Invoice with this merchant_invoice_id "
                "already exists with different data"
            )

        return invoice, False

    return invoice, True