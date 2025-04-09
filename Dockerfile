FROM python:3.11-slim

# Cài poppler-utils và tesseract
RUN apt-get update && \
    apt-get install -y poppler-utils tesseract-ocr libtesseract-dev && \
    apt-get clean

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
