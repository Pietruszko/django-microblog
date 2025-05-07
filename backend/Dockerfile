FROM python:3.10-slim as builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app:/app/backend

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY backend/ .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
