# ==============================================================================
# Stage 1: Build & Dependency Packaging
# ==============================================================================
FROM python:3.11-slim-bookworm AS builder

WORKDIR /build

# Install compilation dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY src/ ./src/

# Build wheels for production dependencies
RUN pip install --no-cache-dir --upgrade pip build \
    && python -m build --wheel --outdir /build/dist \
    && pip wheel --no-cache-dir --wheel-dir /build/wheels fastapi uvicorn pydantic

# ==============================================================================
# Stage 2: Production Runtime
# ==============================================================================
FROM python:3.11-slim-bookworm AS runtime

# OCI Standard Metadata Labels
LABEL org.opencontainers.image.title="Academic Submission Workflow"
LABEL org.opencontainers.image.description="Neutral open-source manuscript submission, editorial desk-review, reviewer assignment engine, and scorecard evaluation platform."
LABEL org.opencontainers.image.source="https://github.com/Borino88/academic-submission-workflow"
LABEL org.opencontainers.image.url="https://fattahi.xyz"
LABEL org.opencontainers.image.documentation="https://github.com/Borino88/academic-submission-workflow#readme"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.authors="Mahdi Fattahi <a.borino88@gmail.com>"

# Create unprivileged non-root runtime user and group
RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -s /bin/bash -m appuser

WORKDIR /app

# Install precompiled wheels from builder stage
COPY --from=builder /build/wheels /tmp/wheels
COPY --from=builder /build/dist /tmp/dist
RUN pip install --no-cache-dir --no-index --find-links=/tmp/wheels /tmp/dist/*.whl \
    && rm -rf /tmp/wheels /tmp/dist

# Set ownership to unprivileged user
RUN chown -R appuser:appgroup /app

# Switch to non-root runtime user
USER appuser

# Health check endpoint verification
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

EXPOSE 8000

# Execute server as non-root user
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
