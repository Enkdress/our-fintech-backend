from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    icon: str
    color: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None


class Category(CategoryBase):
    id: UUID
    user_id: Optional[UUID]  # None for system categories
    is_system: bool
    created_at: datetime
    updated_at: datetime
