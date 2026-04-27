from sqlmodel import Session, select

from app.db.models import CategoryDB

SYSTEM_CATEGORIES = [
    {"name": "Comida",      "icon": "🍜", "color": "#8B6E4E"},
    {"name": "Transporte",  "icon": "🚗", "color": "#4E6E8B"},
    {"name": "Compras",     "icon": "🛍️", "color": "#7A5C7A"},
    {"name": "Salud",       "icon": "💊", "color": "#5C8B6E"},
    {"name": "Hogar",       "icon": "🏠", "color": "#8B7A4E"},
    {"name": "Ocio",        "icon": "🎮", "color": "#6E5C8B"},
    {"name": "Café",        "icon": "☕", "color": "#7A5C4E"},
    {"name": "Gimnasio",    "icon": "💪", "color": "#5C7A8B"},
]


def seed_system_categories(session: Session) -> None:
    existing = session.exec(select(CategoryDB).where(CategoryDB.is_system == True)).all()  # noqa: E712
    if existing:
        return
    for data in SYSTEM_CATEGORIES:
        session.add(CategoryDB(is_system=True, **data))
    session.commit()
