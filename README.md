# our-fintech-backend

FastAPI backend service.

## Requirements

- [uv](https://docs.astral.sh/uv/) — Python package and project manager

Install `uv` if you don't have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Setup

**1. Clone the repo**

```bash
git clone <repo-url>
cd our-fintech-backend
```

**2. Install dependencies**

```bash
uv sync
```

**3. Set up environment variables**

```bash
cp .env.example .env
```

Edit `.env` as needed. See [docs/auth.md](docs/auth.md) for required JWT variables.

**4. Apply migrations**

```bash
uv run alembic upgrade head
```

## Commands

| Command | Description |
|---------|-------------|
| `make install` | Install all dependencies from lockfile |
| `make dev` | Start dev server with hot reload |
| `make test` | Run test suite |
| `make add pkg=<name>` | Add a production dependency |
| `make add-dev pkg=<name>` | Add a dev dependency |

## Running the server

```bash
make dev
```

The API will be available at `http://localhost:8000`.

| URL | Description |
|-----|-------------|
| `http://localhost:8000/api/v1/health` | Health check |
| `http://localhost:8000/docs` | Swagger UI (interactive API docs) |
| `http://localhost:8000/redoc` | ReDoc API docs |

## Documentation

| Topic | File |
|-------|------|
| Authentication (JWT, register, login) | [docs/auth.md](docs/auth.md) |
| Database layer (SQLModel, models, session) | [docs/database.md](docs/database.md) |
| Migrations (Alembic, SQLite quirks) | [docs/migrations.md](docs/migrations.md) |

## Project structure

```
app/
├── main.py              # App entry point, lifespan hooks
├── core/
│   ├── config.py        # Settings loaded from environment / .env
│   └── security.py      # Password hashing and JWT utilities
├── api/
│   ├── deps.py          # Shared dependencies (get_current_user)
│   └── v1/
│       ├── router.py    # API v1 root router
│       ├── auth.py      # Register + login endpoints
│       └── categories.py# Categories CRUD
├── db/
│   ├── models.py        # SQLModel table definitions
│   ├── session.py       # Engine and session dependency
│   └── seed.py          # System category seeding
└── models/              # Pydantic request/response schemas
alembic/
└── versions/            # Migration files
docs/                    # Extended documentation
tests/                   # Pytest test suite
```
