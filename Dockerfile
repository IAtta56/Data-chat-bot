# Build frontend
FROM node:18 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Python backend
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY src/ ./src/
COPY static/ ./static/
COPY uploads/ ./uploads/

# Copy built frontend
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Expose port (Hugging Face Spaces uses 7860)
EXPOSE 7860

# Start the app
CMD ["uvicorn", "src.backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
