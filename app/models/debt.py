from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, computed_field, field_validator


class DebtStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"


class DebtBase(BaseModel):
    label: str
    icon: str
    total_amount: Decimal
    paid_amount: Decimal = Decimal("0")
    due_date: Optional[date] = None

    @field_validator("total_amount")
    @classmethod
    def total_must_be_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("total_amount must be greater than zero")
        return v


class DebtCreate(DebtBase):
    user_id: UUID


class DebtUpdate(BaseModel):
    label: Optional[str] = None
    icon: Optional[str] = None
    paid_amount: Optional[Decimal] = None
    due_date: Optional[date] = None


class DebtPayment(BaseModel):
    amount: Decimal

    @field_validator("amount")
    @classmethod
    def payment_must_be_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("payment amount must be greater than zero")
        return v


class Debt(DebtBase):
    id: UUID
    user_id: UUID
    status: DebtStatus = DebtStatus.ACTIVE
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def remaining_amount(self) -> Decimal:
        return self.total_amount - self.paid_amount

    @computed_field
    @property
    def paid_percentage(self) -> float:
        if self.total_amount == 0:
            return 0.0
        return round(float(self.paid_amount / self.total_amount * 100), 1)

    @computed_field
    @property
    def is_completed(self) -> bool:
        return self.paid_amount >= self.total_amount
