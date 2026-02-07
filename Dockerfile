# 1. Use the official Python lightweight image
FROM python:3.11-slim

# 2. Prevent Python from writing temporary .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Install System Dependencies (Tesseract OCR + Libraries)
# This is the "Secret Sauce" that makes OCR work on any cloud server
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Set the working directory inside the container
WORKDIR /app

# 5. Copy the requirements file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn  # <--- NEW: The Production Server

# 6. Copy the rest of the application code
COPY . .

# 7. The Command to Run the App (Using Gunicorn with 4 Workers)
# This is what prevents crashes. 4 Workers = 4x the power.
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.api:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]