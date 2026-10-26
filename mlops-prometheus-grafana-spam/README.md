# MLOps: Monitor an ML Model Using Prometheus and Grafana

A project monitoring a small SMS spam/ham text classifier with FastAPI, Prometheus, Grafana, and Docker Compose.

> Educational demo only: this classifier uses a tiny hand-written dataset. It is not suitable for real-world spam filtering.

## Requirements
- Docker Desktop installed and running
- Windows PowerShell
- Internet access for the first build

## Start
Run these commands from this folder:

```powershell
docker compose config
docker compose up --build -d
docker compose ps
```

## URLs
- API: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Prometheus metrics: http://localhost:8000/metrics
- Prometheus targets: http://localhost:9090/targets
- Prometheus query UI: http://localhost:9090
- Grafana: http://localhost:3000

Grafana demo login: `admin` / `admin`. Change it if prompted. Never expose these credentials publicly.
The dashboard is provisioned automatically in the **MLOps** folder as **SMS Spam Model Monitoring**.

## Generate traffic
Run in a second PowerShell window:

```powershell
1..30 | ForEach-Object {
    $sample = if ($_ % 2 -eq 0) {
        "Congratulations you won a free prize claim now"
    } else {
        "Hey are we still meeting for lunch today"
    }
    $body = @{ text = $sample } | ConvertTo-Json
    Invoke-RestMethod -Uri "http://localhost:8000/predict" `
        -Method Post -ContentType "application/json" -Body $body
}
```

Wait for a few Prometheus scrapes, then refresh Grafana. Use the Last 15 minutes time range.
The model is intentionally small; predictions are illustrative and can be wrong.

## Metrics
- `model_http_requests_total`: requests by method, endpoint, and status
- `model_http_request_duration_seconds`: HTTP latency histogram
- `model_predictions_total`: predictions by predicted class
- `model_prediction_errors_total`: caught prediction failures
- `model_prediction_confidence`: histogram of maximum predicted probability

## Troubleshooting
```powershell
docker compose ps
docker compose logs --tail 100 model-api
docker compose logs --tail 100 prometheus
docker compose logs --tail 100 grafana
```

After code/config changes:
```powershell
docker compose up --build -d
```

Stop the services:
```powershell
docker compose down
```
Named data volumes are preserved. `docker compose down -v` also deletes stored monitoring data.

## What this assignment demonstrates
- Containerized model serving
- Prometheus instrumentation and scraping
- Time-series metrics
- Grafana dashboard provisioning
- Operational monitoring

Operational monitoring does not prove model accuracy or detect data drift; those require labeled data or input-distribution checks.
