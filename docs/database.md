# Database Layer

SQLite in development, driven by SQLModel (SQLAlchemy + Pydantic unified).

## Configuration

The database URL is set via `DATABASE_URL` in `.env`:

```
DATABASE_URL=sqlite:///./tuplan.db
```

The file `tuplan.db` is gitignored.

## Session

`app/db/session.py` exposes two things:

- **`engine`** — shared SQLAlchemy engine (used by Alembic and the lifespan seed)
- **`get_session()`** — FastAPI dependency that yields a `Session` per request

```python
from app.db.session import get_session
from sqlmodel import Session

@router.get("/example")
def example(session: Session = Depends(get_session)):
    ...
```

## Models

All DB tables are defined in `app/db/models.py` as SQLModel classes with `table=True`.

| Class | Table | Description |
|---|---|---|
| `UserDB` | `users` | Registered users with hashed password and preferences |
| `CategoryDB` | `categories` | System and user-owned expense categories |
| `TransactionDB` | `transactions` | Individual income/expense entries |
| `BudgetDB` | `budgets` | Monthly budget limits per user |
| `DebtDB` | `debts` | Tracked debts with paid/total amounts |

`CategoryDB.user_id` is `NULL` for system categories (visible to all users) and set to the owner's UUID for custom categories.

## Startup

`app/main.py` uses the FastAPI lifespan hook to run two things on every startup:

1. `create_db_and_tables()` — creates any missing tables (safe to run repeatedly)
2. `seed_system_categories()` — inserts the 8 built-in categories if the table is empty

The seed is idempotent: it checks for existing system categories before inserting.

## Pydantic models vs DB models

`app/db/models.py` contains the ORM layer (`*DB` classes). `app/models/` contains the Pydantic schemas used for request/response serialization (`Category`, `CategoryCreate`, etc.). Keep them separate — the API layer should never expose `*DB` objects directly.
