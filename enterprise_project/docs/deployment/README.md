# Deployment & Runbook
1. Build: `docker build -f docker/Dockerfile -t ecommerce-api .`
2. Local stack: `SECRET_KEY=... docker compose -f docker/docker-compose.yml up`
3. K8s: create secret `kubectl create secret generic ecommerce-secrets --from-literal=secret-key=...`, then `scripts/deploy.sh <image>`
4. Migrations: `python -m src.core.migrate`
5. Rollback: `kubectl rollout undo deployment/ecommerce-api`

## Runbook
- **HighErrorRate**: check `kubectl logs`, recent deploy -> rollback.
- **HighLatencyP95**: check DB, scale replicas.
- **ServiceDown**: check pod status/probes, events.
