#!/usr/bin/env bash
set -euo pipefail
IMAGE="${1:?usage: deploy.sh <image:tag>}"
kubectl apply -f kubernetes/configmap.yaml -f kubernetes/service.yaml -f kubernetes/ingress.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl set image deployment/ecommerce-api api="$IMAGE"
kubectl rollout status deployment/ecommerce-api --timeout=120s
