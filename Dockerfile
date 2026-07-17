FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src

COPY config/ ./config

RUN mkdir -p /app/logs && \
    useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

CMD ["python", "./src/main.py"]