from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class Currency(str, Enum):
    COP = "COP"
    USD = "USD"
    EUR = "EUR"


class Language(str, Enum):
    ES = "es"
    EN = "en"


class UserPreferences(BaseModel):
    currency: Currency = Currency.COP
    language: Language = Language.ES
    monthly_budget: float = 0.0
    dark_mode: bool = True
    notifications_enabled: bool = True
    face_id_enabled: bool = False
    pin_configured: bool = False


class UserBase(BaseModel):
    name: str
    email: str
    preferences: UserPreferences = UserPreferences()


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    preferences: Optional[UserPreferences] = None


class User(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
