FROM python:3.11-slim

LABEL description="Attack Simulator — Controlled Safe Attacker"

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Simulator only needs httpx
RUN pip install --no-cache-dir httpx python-dotenv

COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

CMD ["python", "main.py"]
