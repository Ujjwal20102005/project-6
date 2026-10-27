# Architecture
Layered design: **API (routes) -> Services (business logic) -> Models (SQLAlchemy) -> DB**.
Cross-cutting: middleware (logging, metrics, rate limit, security headers), config via env vars.

```
Client -> Ingress(TLS) -> FastAPI pods (x3) -> PostgreSQL
                              |-> /metrics -> Prometheus -> Grafana/Alerts
```
Microservice path: split `ProductService`, `OrderService`, `UserService` into separate deployables behind an API gateway;
the service layer already isolates each domain. Scaling: stateless pods (HPA), swap in-memory rate limiter for Redis, add caching.
