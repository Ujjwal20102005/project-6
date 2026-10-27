# Enterprise E-Commerce Platform
Production-oriented FastAPI e-commerce backend: JWT/RBAC auth, products, orders with stock checks,
Prometheus metrics, rate limiting, Docker, Kubernetes, GitHub Actions CI/CD, and 94% test coverage.

Includes a built-in web storefront (`src/static/index.html`): browse products, cart, sign in/register, checkout, order history, and an admin form to add products.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python -m src.utils.seed          # admin@example.com / ChangeMe123!
python -m src.main                # Storefront UI: http://localhost:8000/  ·  API docs: /docs
pytest                            # tests + coverage gate (>=85%)
```
## Structure
`src/` (api, core, models, services, middleware, config, utils) · `tests/` (unit, integration, e2e, performance) ·
`docker/` · `kubernetes/` · `.github/workflows/` · `monitoring/` · `security/` · `performance/` · `migrations/` · `docs/` · `scripts/`

## Testing evidence
See `tests/`; `pytest` prints a coverage report. Add screenshots of `/docs` and Grafana to `docs/user/`.
## Notes
Default DB is SQLite for local use; set `DATABASE_URL` to Postgres in production (add `psycopg2-binary`).
