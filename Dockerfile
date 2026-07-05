FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir flask gunicorn
COPY src/ ./src/

ENV PORT=8080
EXPOSE 8080
USER nobody
CMD ["gunicorn", "--pythonpath", "src", "api:app", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120"]
