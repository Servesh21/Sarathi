FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

RUN python3 -m venv .venv
RUN .venv/bin/pip install --no-cache-dir -r requirements.txt



# Copy application
COPY . .

# Create upload directory
RUN mkdir -p /app/uploads /app/chroma_data

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
