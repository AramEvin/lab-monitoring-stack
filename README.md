# SOC Lab Monitoring Stack

A hands-on, fully Dockerized lab for learning **Prometheus**, **Alertmanager**, and **Grafana** — built to simulate a multi-tenant SOC (Security Operations Center) backend with synthetic metrics.

No real infrastructure required. Everything runs in containers with a fake metrics generator standing in for real services, so you can learn the full monitoring pipeline end-to-end: **scrape → alert → visualize → verify via API.**

## What you'll learn

- Writing Prometheus scrape configs and alert rules
- Routing alerts through Alertmanager to a webhook receiver
- Provisioning Grafana datasources as code (no manual UI clicking)
- Authenticating against the Grafana API with scoped service-account tokens
- Verifying a monitoring stack at every layer: internal networking, external ports, and end-to-end data flow

## Architecture

```
metrics-generator ──scrape──▶ prometheus ──alerts──▶ alertmanager ──webhook──▶ webhook-sink
                                    │
                                    └────▶ grafana (datasource: Lab-Prometheus)
```

| Service | Image | Port |
|---|---|---|
| Prometheus | `prom/prometheus:v2.53.0` | 9090 |
| Alertmanager | `prom/alertmanager:v0.27.0` | 9093 |
| Grafana | `grafana/grafana-oss:11.1.0` | 3000 |
| metrics-generator | built from `./generator` | 8000 |
| webhook-sink | built from `./webhook-sink` | 8080 |

## Prerequisites

- Ubuntu (or any Linux host / WSL2)
- `curl`, `openssl`, `python3`
- No Docker required beforehand — Step 1 installs it

## Quick Start

```bash
git clone https://github.com/<your-username>/soc-lab-monitoring-stack.git
cd soc-lab-monitoring-stack

# 1. Generate credentials (never hardcoded)
export GRAFANA_ADMIN_USER="admin"
export GRAFANA_ADMIN_PASSWORD="$(openssl rand -base64 16)"

# 2. Start the stack
docker compose up -d --build

# 3. Check everything is healthy
bash scripts/health-check.sh
```

Then open:
- Grafana → http://localhost:3000 (login with the generated credentials above)
- Prometheus → http://localhost:9090
- Alertmanager → http://localhost:9093

## Full Setup Guide

The complete 15-step walkthrough — with the reasoning behind every command, not just the command itself — is in [`docs/SOC_Lab_Monitoring_Stack_Setup_Guide.docx`](docs/SOC_Lab_Monitoring_Stack_Setup_Guide.docx):

1. Environment variables & credential handling
2. Install Docker (official repo, not the outdated Ubuntu package)
3. Project directory structure
4. Prometheus scrape config + alert rules (validated with `promtool`)
5. Synthetic metrics generator (Python, multi-tenant)
6. Alertmanager + webhook receiver
7. Grafana datasource provisioning as code
8. `docker-compose.yml` — all 5 services, pinned versions
9. Start the stack & verify actual binary versions (not just image tags)
10. Internal container-to-container connectivity checks
11. External (host) reachability checks
12. Grafana API authentication via service-account token
13. Fetch datasource UID programmatically (no hardcoded UIDs)
14. End-to-end PromQL check through Grafana's own query API
15. One-script full health check

## Project Structure

```
.
├── docker-compose.yml
├── prometheus/
│   ├── prometheus.yml
│   └── alert-rules.yml
├── generator/
│   ├── generate_metrics.py
│   ├── requirements.txt
│   └── Dockerfile
├── alertmanager/
│   └── alertmanager.yml
├── webhook-sink/
│   ├── app.py
│   └── Dockerfile
├── grafana/
│   └── provisioning/datasources/datasource.yml
├── scripts/
│   └── health-check.sh
└── docs/
    └── SOC_Lab_Monitoring_Stack_Setup_Guide.docx
```

## Health Check

Run the full smoke test any time (after a restart, upgrade, or config change):

```bash
bash scripts/health-check.sh
```

Checks: Docker versions, container status, internal service-to-service connectivity, and external port reachability.

## Roadmap

- [ ] Step 15: credential rotation (regenerate Grafana password/token without downtime)
- [ ] Add pre-built Grafana dashboard JSON
- [ ] Slack/Telegram receiver in place of the dummy webhook

## License

MIT — use freely for learning, labs, or internal training.

## Trademark Notice

Grafana and the Grafana logo are trademarks of Grafana Labs. Prometheus and the Prometheus logo are trademarks of The Linux Foundation. This project is an independent educational lab and is not affiliated with either project.
