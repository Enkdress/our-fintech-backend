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

This creates a virtual environment at `.venv/` and installs all dependencies (including dev) from `uv.lock`.

**3. Set up environment variables**

```bash
cp .env.example .env
```

Edit `.env` as needed.

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

## Running tests

```bash
make test
```

## Adding dependencies

```bash
# Production dependency
make add pkg=<package>

# Dev-only dependency
make add-dev pkg=<package>
```

Always commit both `pyproject.toml` and `uv.lock` after adding dependencies.

## Project structure

```
app/
├── main.py          # App entry point, router registration
├── core/
│   └── config.py    # Settings loaded from environment / .env
├── api/
│   └── v1/
│       └── router.py  # API v1 routes
└── models/          # Pydantic models
tests/               # Pytest test suite
```
