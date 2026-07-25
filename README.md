# Academic Submission Workflow (`academic-submission-workflow`)

[![CI & Docker Publish](https://github.com/Borino88/academic-submission-workflow/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/Borino88/academic-submission-workflow/actions/workflows/docker-publish.yml)
[![Docker Pulls](https://img.shields.io/badge/Docker%20Hub-borino88%2Facademic--submission--workflow-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://app.docker.com/repository/docker/borino88/academic-submission-workflow)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](./LICENSE)

A neutral open-source manuscript submission, editorial desk-review, reviewer assignment engine, and scorecard evaluation platform engineered by **Mahdi Fattahi**. Built specifically to decouple scientific peer evaluation from commercial publishing constraints and proprietary branding.

---

## 🐳 Docker Container Quick-Start

The platform is packaged as a hardened, multi-stage Docker container executing strictly under an unprivileged non-root user (`appuser`, UID `1000`) and compiled for multi-architecture deployments (`linux/amd64`, `linux/arm64`).

### 1. Docker Pull Command
```bash
docker pull borino88/academic-submission-workflow:latest
```

### 2. Supported Tags & Architectures
* **Tags:** `1.0.0`, `1.0`, `1`, `latest`, `main`
* **Architectures:** `linux/amd64`, `linux/arm64`
* **Docker Hub Repository:** [borino88/academic-submission-workflow](https://app.docker.com/repository/docker/borino88/academic-submission-workflow)

### 3. Docker Compose Instructions
Launch the submission platform in an isolated multi-container stack:
```yaml
version: '3.8'
services:
  workflow-engine:
    image: borino88/academic-submission-workflow:latest
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
    user: "1000:1000"
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 5s
      retries: 3
```

---

## 🛠️ Key Workflow Capabilities

1. **Author Submission Portal:** Ingests manuscript abstracts, metadata, and cryptographic SHA-256 file hashes (`POST /api/v1/manuscripts/submit`).
2. **Editorial Desk Review:** Enforces role-based authority (`EDITOR` role required) for assigning managing editors and inviting peer reviewers.
3. **Structured Review Scorecards:** Evaluates submissions across standardized 1-5 methodology, clarity, and reproducibility dimensions.
4. **Immutable Audit Ledger:** Automatically records every editorial transition and peer evaluation with UTC timestamps.

---

## 🔒 Security & Publisher Privacy Statement

This codebase contains **zero commercial publisher branding, zero MDPI references, and zero SuSy workflows**. All included sample manuscripts are 100% synthetic, open-source simulations designed for algorithmic verification.
