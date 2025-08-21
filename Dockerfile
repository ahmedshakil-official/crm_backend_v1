FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system dependencies for psycopg2 and other packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install project dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY install-weasyprint-deps.sh /app/
RUN chmod +x /app/install-weasyprint-deps.sh && /app/install-weasyprint-deps.sh

# Copy application files
COPY . /app/

# Expose the port Django will run on
EXPOSE 5000
