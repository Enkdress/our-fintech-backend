from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, computed_field, field_validator


class BudgetBase(BaseModel):
    year: int
    month: int
    limit_amount: Decimal
    spent_amount: Decimal = Decimal("0")

    @field_validator("month")
    @classmethod
    def month_must_be_valid(cls, v: int) -> int:
        if not 1 <= v <= 12:
            raise ValueError("month must be between 1 and 12")
        return v

    @field_validator("limit_amount")
    @classmethod
    def limit_must_be_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("limit_amount must be greater than zero")
        return v


class BudgetCreate(BudgetBase):
    user_id: UUID


class BudgetUpdate(BaseModel):
    limit_amount: Optional[Decimal] = None
    spent_amount: Optional[Decimal] = None


class Budget(BudgetBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def remaining_amount(self) -> Decimal:
        return self.limit_amount - self.spent_amount

    @computed_field
    @property
    def usage_percentage(self) -> float:
        if self.limit_amount == 0:
            return 0.0
        return round(float(self.spent_amount / self.limit_amount * 100), 1)
