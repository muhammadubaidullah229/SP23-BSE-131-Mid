# ===================================================================
# Dockerfile for SP23-BSE-131-Mid
# Course: DevOps for Cloud Computing (CSC418)
# Multi-container Web Application Deployment
# ===================================================================

# Step 1: Base Python 3.11 slim image
FROM python:3.11-slim AS base

# Step 2: Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Step 3: Set working directory inside container
WORKDIR /app

# Step 4: Install system dependencies (curl for healthchecks, gcc/libpq-dev for postgresql client)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Step 5: Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Step 6: Create a non-root user for security (Linux Principle of Least Privilege)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

# Step 7: Copy application source code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Step 8: Expose application port
EXPOSE 5000

# Step 9: Container Health Check (verifies app is responsive on /health)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Step 10: Run the application using Gunicorn production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--timeout", "60", "run:app"]
