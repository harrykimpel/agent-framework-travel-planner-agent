# Deployment Guide

This document describes how to run and deploy the AI Travel Planner sample in development and production environments.

## Running Locally (recommended for development)

1. Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# or
# .venv\Scripts\activate   # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables by creating a `.env` file (see README.md for variables).

4. Run the helper script:

```bash
./run.sh
```

The `run.sh` script runs `streamlit run web_app.py` and ensures the environment is loaded from `.env`.

## Docker (local container)

Create a `Dockerfile` (example below) to containerize the app.

Example `Dockerfile` (simple):

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
ENV PORT=8501
EXPOSE 8501
CMD ["streamlit", "run", "web_app.py", "--server.port=8501", "--server.headless=true"]
```

Build and run:

```bash
docker build -t travel-planner:latest .
docker run --rm -p 8501:8501 --env-file .env travel-planner:latest
```

Note: pass sensitive keys via a secrets manager or environment injection in CI/CD — avoid embedding them in the image.

## Production Deployment Options

- **Azure Container Instances / Azure App Service**: Deploy the built container image. Configure environment variables in the platform settings. Ensure outbound network and secrets are protected.
- **Kubernetes / AKS**: Run as a Deployment with a Service and an Ingress. Use a Secret store for API keys.
- **Cloud Run (GCP)** or **AWS Fargate**: Deploy the container image and set environment variables/secrets accordingly.

## Observability in Production

- Ensure OTLP exporter endpoint and New Relic ingest keys are provisioned as environment variables.
- Limit or sanitize sensitive data before exporting spans if required by policy.
- Configure sampling for traces to control telemetry costs.

## Scaling Considerations

- The sample app is single-process; for production behind a load balancer use a container orchestrator with multiple replicas.
- Streamlit is primarily intended for single-server UIs — for heavy scale or multi-user concurrency consider converting to a web framework plus front-end (FastAPI + React) and using the agent as an async microservice.

## Secrets & Configuration

- Store `GITHUB_TOKEN`, `OPENWEATHER_API_KEY`, and New Relic keys in a secure secret store (Azure Key Vault, AWS Secrets Manager, etc.).
- Use least-privilege tokens for third-party APIs.

## Health Checks & Monitoring

- Expose a simple health endpoint in a wrapper service, or use process-level checks. Monitor CPU/memory and request latency via New Relic.

## Example CI/CD Steps (high level)

1. Build the Docker image in your CI pipeline.
2. Push the image to your registry (Docker Hub, ACR, ECR, GCR).
3. Deploy via your chosen platform (Helm chart, GitHub Actions to Azure, Cloud Run, etc.).
4. Run smoke tests that hit the root UI and a sample itinerary generation.

---

If you want, I can add a sample `Dockerfile`, a `docker-compose.yml`, and a GitHub Actions workflow for building and pushing the image.
