# API
Interactive OpenAPI docs: `/docs` (Swagger) and `/redoc` when `DEBUG=true`; schema at `/openapi.json`.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | /auth/register | - | Create account |
| POST | /auth/login | - | Get JWT |
| GET | /products | - | List (skip, limit) |
| POST | /products | admin | Create product |
| POST | /orders | user | Place order (checks stock) |
| GET | /orders | user | My orders |
| GET | /health, /metrics | - | Health, Prometheus |
