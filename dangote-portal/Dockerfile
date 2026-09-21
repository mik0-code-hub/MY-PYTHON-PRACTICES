# Use lightweight official Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing .pyc and buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose port (default 8000)
EXPOSE 8000

# Run Uvicorn ASGI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
