# Multi-stage build for React + FastAPI
FROM node:18-alpine AS frontend-build

# Set working directory
WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY frontend/ ./

# Build React app
RUN npm run build

# Python backend stage
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/
COPY src/ ./src/

# Copy built React app from frontend stage
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Create keep-alive script
RUN echo '#!/bin/bash\nwhile true; do\n  curl -f http://localhost:8080/api/health > /dev/null 2>&1 || true\n  sleep 300\ndone' > /app/keep-alive.sh && chmod +x /app/keep-alive.sh

# Expose port
EXPOSE 8080

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8080

# Start keep-alive in background and run the app
CMD /app/keep-alive.sh & uvicorn backend.main:app --host 0.0.0.0 --port 8080