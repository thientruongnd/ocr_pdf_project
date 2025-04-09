FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y poppler-utils tesseract-ocr \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "--workers", "2", "-k", "uvicorn.workers.UvicornWorker"]
