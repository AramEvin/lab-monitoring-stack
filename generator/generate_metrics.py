import os, random, threading, time
from prometheus_client import start_http_server, Counter, Gauge

TENANTS = os.environ.get("TENANTS", "tenant_alpha,tenant_beta").split(",")
events_ingested = Counter("soc_events_ingested_total", "events", ["tenant"])
alerts_total = Counter("soc_alerts_total", "alerts", ["tenant", "severity"])
agent_status = Gauge("soc_agent_status", "status", ["tenant", "agent_id"])
ingestion_lag = Gauge("soc_ingestion_lag_seconds", "lag", ["tenant"])

def simulate():
    while True:
        for t in TENANTS:
            events_ingested.labels(tenant=t).inc(random.randint(50, 400))
            if random.random() < 0.35:
                sev = random.choice(["critical","high","medium","low"])
                alerts_total.labels(tenant=t, severity=sev).inc(random.randint(1,5))
            ingestion_lag.labels(tenant=t).set(round(random.uniform(0.2,4.5),2))
            for i in range(1,6):
                agent_status.labels(tenant=t, agent_id=f"{t}-agent-{i}").set(1)
        time.sleep(5)

threading.Thread(target=simulate, daemon=True).start()
start_http_server(8000)
while True: time.sleep(3600)
