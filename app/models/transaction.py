from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class TransactionBase(BaseModel):
    amount: Decimal
    type: TransactionType
    category_id: UUID
    description: str
    date: date

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("amount must be greater than zero")
        return v


class TransactionCreate(TransactionBase):
    user_id: UUID


class TransactionUpdate(BaseModel):
    amount: Optional[Decimal] = None
    category_id: Optional[UUID] = None
    description: Optional[str] = None
    date: Optional[date] = None


class Transaction(TransactionBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
