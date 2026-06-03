# Orders Service

A Flask-based e-commerce backend that handles users, products, orders, payments, and inventory.

## Quick Start

```bash
pip install -r requirements.txt
python -m scripts.seed
python run.py
```

Server runs on port 5000.

## Architecture

- **API v2** (`/api/v2/*`): JWT-authenticated REST endpoints, repository + service layer.
- **API v1** (`/api/v1/*`): mixed — products/inventory use repositories directly; orders/users use legacy session-based auth.
- **Legacy** (`app/legacy/`): older endpoints kept for backward compatibility. Scheduled for deprecation.

## Authentication

- v2 endpoints: JWT tokens via `Authorization: Bearer <token>`
- v1 orders/users (legacy): Flask session cookies
- v1 products: public (no auth)

## Tech Stack

- Flask
- SQLite (production uses Postgres via `DATABASE_URL`)
- PyJWT for tokens
- In-memory cache (Redis planned)
- Stripe for payments

## Background Tasks

Currently synchronous. See `app/tasks/jobs.py`. Celery migration is in progress.

## Database

Schema is defined in `app/db.py`. Migration files exist under `migrations/` but are not currently applied by any automated tool.

## Endpoints (partial list)

### Users (v2)
- `POST /api/v2/users/register`
- `POST /api/v2/users/login`
- `GET /api/v2/users/me`

### Orders (v2)
- `POST /api/v2/orders/` — create
- `GET /api/v2/orders/` — list mine
- `POST /api/v2/orders/<id>/pay`
- `POST /api/v2/orders/<id>/cancel`

### Products (v1)
- `GET /api/v1/products/`
- `GET /api/v1/products/<id>`
- `GET /api/v1/products/search?q=...`

### Inventory (v1)
- `POST /api/v1/inventory/<id>/adjust` (admin)
- `GET /api/v1/inventory/<id>/history` (admin)
- `GET /api/v1/inventory/low-stock`

### Webhooks
- `POST /api/v2/webhooks/stripe`

## Known Issues / TODO

- Stock decrement is not transactional with order creation
- Cancel doesn't restore inventory
- Webhook signature verification is stubbed
- Two password hashing algorithms in use (PBKDF2 in new code, SHA1 in legacy)
- In-memory rate limiter doesn't share state across workers

## Testing

```bash
pytest
```

Coverage is partial. Cancel/refund flow, legacy endpoints, and rate limiting aren't tested.
