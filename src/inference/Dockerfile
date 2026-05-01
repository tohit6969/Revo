# Use slim Python; swap for CUDA base if you need GPU support
FROM python:3.10-slim

WORKDIR /app

# Install inference deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model code and weights
COPY . .

# Default command just prints help; the backend will invoke this script
CMD ["python", "run_inference.py", "--help"]
