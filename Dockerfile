# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Expose Flask on port 8080 (Cloud Run default)
ENV PORT 8080

# Start app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "run:app"]
