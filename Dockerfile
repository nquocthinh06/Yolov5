FROM python:3.10-slim

# System deps: ffmpeg (for OpenCV video I/O) and X libs for image windows if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    git ffmpeg libsm6 libxext6 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Use existing project requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Env defaults
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=Asia/Ho_Chi_Minh

# Default command prints help; override at run time to train/infer as needed
CMD ["python", "train_traffic_signs.py", "--help"]


