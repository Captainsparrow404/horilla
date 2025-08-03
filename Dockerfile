FROM python:3.10-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libcairo2-dev \
    gcc \
    libpq-dev \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# ✅ Make start.sh executable
RUN chmod +x start.sh

# Expose port for the app
EXPOSE 8000

# ✅ Run start script at container startup (runs migrations, collectstatic, gunicorn)
CMD ["./start.sh"]
