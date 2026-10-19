# BNPL Customer Service

Django REST Framework identity/customer service. Uses a UUID user ID, email login, JWT access and rotating refresh tokens, Django Admin, and token blacklist for logout.

## Local setup

```bash
cd services/customer
uv sync
cp .env.example .env
# Start PostgreSQL and create database bnpl_customer or set DATABASE_URL=sqlite:///db.sqlite3 for a disposable local demo.
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver 8002
```

Test: `uv run python manage.py test customers`

Endpoints:
- `GET /health/` public
- `POST /api/v1/auth/register/` with email, password, first_name, last_name
- `POST /api/v1/auth/login/` with email, password
- `POST /api/v1/auth/refresh/` with refresh
- `POST /api/v1/auth/logout/` with refresh (revokes refresh token, not previously issued access tokens)
- `GET/PATCH /api/v1/customers/me/` Bearer access token
- `/admin/` Django admin session authentication

## Security notes
- For now tokens are **HS256** signed, suitable for a local standalone demo. Do **not** copy the signing key into every microservice. Before configuring other services to verify access tokens, move to **RS256** with a private key only in customer and public key in consumers. Validate issuer, audience, expiry and authorized scopes/roles. Do not treat `is_staff` as an API role.
- Run with HTTPS, private secrets, stable DB-backed throttling (e.g. Redis) for production; DRF throttling alone is not a security-grade brute-force defense. Add login lockout/rate limiting at edge.
- A previously issued access JWT remains valid until expiry after logout or user deactivation unless services query revocation/user status.
- Configure SMTP/email verification, password reset, account deletion, audit logs, key rotation and privacy controls before handling real users.
- The default SQLite DB is only a convenience for local smoke tests; use PostgreSQL for this project's deployment.
