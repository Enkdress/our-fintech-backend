from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_current_user
from app.db.models import CategoryDB, UserDB
from app.db.session import get_session
from app.models.category import Category, CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[Category])
def list_categories(
    current_user: UserDB = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> list[Category]:
    rows = session.exec(
        select(CategoryDB).where(
            (CategoryDB.is_system == True) | (CategoryDB.user_id == current_user.id)
        )
    ).all()
    return [Category.model_validate(r, from_attributes=True) for r in rows]


@router.post("", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    current_user: UserDB = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Category:
    category = CategoryDB(
        user_id=current_user.id,
        name=payload.name,
        icon=payload.icon,
        color=payload.color,
        is_system=False,
    )
    session.add(category)
    session.commit()
    session.refresh(category)
    return Category.model_validate(category, from_attributes=True)


@router.patch("/{category_id}", response_model=Category)
def update_category(
    category_id: UUID,
    payload: CategoryUpdate,
    current_user: UserDB = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Category:
    category = session.get(CategoryDB, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    if not category.is_system and category.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot modify this category")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(category, field, value)

    session.add(category)
    session.commit()
    session.refresh(category)
    return Category.model_validate(category, from_attributes=True)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: UUID,
    current_user: UserDB = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> None:
    category = session.get(CategoryDB, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    if not category.is_system and category.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete this category")

    session.delete(category)
    session.commit()
