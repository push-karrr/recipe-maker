# -------- Stage 1: Builder --------
FROM python:3.13-slim as builder

WORKDIR /install

# Install build dependencies required for bcrypt, psycopg2, etc.
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install packages globally
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# -------- Stage 2: Final --------
FROM python:3.13-slim

WORKDIR /app

# Install only runtime dependencies (for bcrypt to run)
RUN apt-get update && apt-get install -y \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy installed site-packages and binaries from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
