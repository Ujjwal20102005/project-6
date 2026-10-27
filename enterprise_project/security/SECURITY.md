# Security Policy
Report vulnerabilities privately to security@example.com. Do not open public issues.

## Controls implemented
- JWT bearer auth (HS256, expiring tokens) and role-based access (admin/customer)
- PBKDF2-SHA256 password hashing (120k iterations, per-user salt)
- Per-IP rate limiting, security headers (HSTS, nosniff, X-Frame-Options)
- Trusted host + CORS allow-lists, docs disabled when DEBUG=false
- Input validation via Pydantic; parameterized queries via SQLAlchemy
- Non-root container, multi-stage image; `bandit` scan in CI

## Before production
Set a strong SECRET_KEY, restrict CORS/hosts, use Postgres and a Redis-backed rate limiter,
add refresh-token rotation, and store secrets in a secret manager.
