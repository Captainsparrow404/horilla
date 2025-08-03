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

# Copy project files into the container
COPY . .

# 🔐 Make the shell script executable (adjust the name if different)
RUN chmod +x ./start.sh

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# ✅ Use the executable shell script to start your app (adjust path if needed)
CMD ["./start.sh"]
