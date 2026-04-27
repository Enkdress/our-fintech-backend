from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Column, Numeric
from sqlmodel import Field, SQLModel


class UserDB(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    hashed_password: str
    currency: str = Field(default="COP", max_length=3)
    language: str = Field(default="es", max_length=5)
    monthly_budget: Decimal = Field(
        default=Decimal("0"), sa_column=Column(Numeric(15, 2), nullable=False, default=0)
    )
    dark_mode: bool = Field(default=True)
    notifications_enabled: bool = Field(default=True)
    face_id_enabled: bool = Field(default=False)
    pin_configured: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CategoryDB(SQLModel, table=True):
    __tablename__ = "categories"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    # NULL user_id = system category available to everyone
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id", index=True)
    name: str
    icon: str = Field(max_length=10)
    color: str = Field(max_length=9)  # hex e.g. "#8B6E4E"
    is_system: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TransactionDB(SQLModel, table=True):
    __tablename__ = "transactions"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    category_id: uuid.UUID = Field(foreign_key="categories.id", index=True)
    amount: Decimal = Field(sa_column=Column(Numeric(15, 2), nullable=False))
    type: str
    description: str
    date: date
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class BudgetDB(SQLModel, table=True):
    __tablename__ = "budgets"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    year: int
    month: int
    limit_amount: Decimal = Field(sa_column=Column(Numeric(15, 2), nullable=False))
    spent_amount: Decimal = Field(
        default=Decimal("0"), sa_column=Column(Numeric(15, 2), nullable=False, default=0)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DebtDB(SQLModel, table=True):
    __tablename__ = "debts"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    label: str
    icon: str = Field(max_length=10)
    total_amount: Decimal = Field(sa_column=Column(Numeric(15, 2), nullable=False))
    paid_amount: Decimal = Field(
        default=Decimal("0"), sa_column=Column(Numeric(15, 2), nullable=False, default=0)
    )
    due_date: Optional[date] = None
    status: str = Field(default="active")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
