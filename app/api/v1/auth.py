from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import UserDB
from app.db.session import get_session
from app.models.user import Currency, Language, Token, User, UserCreate, UserLogin, UserPreferences

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, session: Session = Depends(get_session)) -> Token:
    existing = session.exec(select(UserDB).where(UserDB.email == payload.email)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = UserDB(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        currency=payload.preferences.currency.value,
        language=payload.preferences.language.value,
        monthly_budget=payload.preferences.monthly_budget,
        dark_mode=payload.preferences.dark_mode,
        notifications_enabled=payload.preferences.notifications_enabled,
        face_id_enabled=payload.preferences.face_id_enabled,
        pin_configured=payload.preferences.pin_configured,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return Token(access_token=create_access_token(str(user.id)))


@router.post("/login", response_model=Token)
def login(payload: UserLogin, session: Session = Depends(get_session)) -> Token:
    user = session.exec(select(UserDB).where(UserDB.email == payload.email)).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return Token(access_token=create_access_token(str(user.id)))


@router.get("/me", response_model=User)
def me(current_user: UserDB = Depends(get_current_user)) -> User:
    return User(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        preferences=UserPreferences(
            currency=Currency(current_user.currency),
            language=Language(current_user.language),
            monthly_budget=float(current_user.monthly_budget),
            dark_mode=current_user.dark_mode,
            notifications_enabled=current_user.notifications_enabled,
            face_id_enabled=current_user.face_id_enabled,
            pin_configured=current_user.pin_configured,
        ),
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )
