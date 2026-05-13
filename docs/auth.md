# Authentication

JWT-based auth using HS256. Tokens are issued on register and login and must be sent as a Bearer header on all protected routes.

## Configuration

All values are read from `.env` (see `app/core/config.py`):

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `change-me-in-production` | HMAC signing key — **change this in production** |
| `ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `10080` (7 days) | Token lifetime |

## Endpoints

### Register

```
POST /api/v1/auth/register
```

Creates a new user and returns a token.

```json
// Request
{
  "name": "Sergio",
  "email": "sergio@example.com",
  "password": "mypassword",
  "preferences": {
    "currency": "COP",
    "language": "es",
    "monthly_budget": 0,
    "dark_mode": true,
    "notifications_enabled": true,
    "face_id_enabled": false,
    "pin_configured": false
  }
}

// Response 201
{ "access_token": "<jwt>", "token_type": "bearer" }
```

Returns `409` if the email is already registered.

### Login

```
POST /api/v1/auth/login
```

```json
// Request
{ "email": "sergio@example.com", "password": "mypassword" }

// Response 200
{ "access_token": "<jwt>", "token_type": "bearer" }
```

Returns `401` on wrong email or password.

## Using the token

Pass the token as a Bearer header on all protected routes:

```
Authorization: Bearer <jwt>
```

## Implementation

- **`app/core/security.py`** — password hashing (`bcrypt` directly, not passlib) and JWT encode/decode
- **`app/api/v1/auth.py`** — register and login route handlers
- **`app/api/deps.py`** — `get_current_user` FastAPI dependency; inject it into any route that needs the authenticated user

```python
from app.api.deps import get_current_user
from app.db.models import UserDB

@router.get("/me")
def me(current_user: UserDB = Depends(get_current_user)):
    return current_user
```

> **Note on bcrypt**: passlib 1.7.4 is incompatible with bcrypt 5.x. The project uses bcrypt's API directly (`bcrypt.hashpw` / `bcrypt.checkpw`) to avoid this.
