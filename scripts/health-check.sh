#!/usr/bin/env bash
# Full stack health check — Prometheus / Alertmanager / Grafana / metrics-generator
set -uo pipefail

echo "=== Docker versions ==="
docker --version
docker compose version

echo "=== Container status ==="
docker compose ps --format "table {{.Name}}\t{{.Status}}"

echo "=== Internal connectivity ==="
docker compose exec -T prometheus wget -qO- http://metrics-generator:8000/metrics > /dev/null \
  && echo "prometheus -> generator: OK"
docker compose exec -T grafana wget -qO- http://prometheus:9090/-/healthy > /dev/null \
  && echo "grafana -> prometheus: OK"

echo "=== External endpoints ==="
for url in "http://localhost:9090/-/healthy" "http://localhost:9093/-/healthy" \
           "http://localhost:3000/api/health" "http://localhost:8000/metrics"; do
  status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  echo "$url -> HTTP $status"
done
