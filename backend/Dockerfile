FROM python:3.11

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    inotify-tools \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install watchdog

# Copy the rest of the application
COPY . .

# Expose the application port
EXPOSE 8000

# Set the default command to run the backend
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
