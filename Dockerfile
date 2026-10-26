FROM python:3.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    ASR_DATASET_DIR=/app/dataset \
    HF_HOME=/home/asr/.cache/huggingface \
    XDG_CACHE_HOME=/home/asr/.cache \
    DISABLE_SAFETENSORS_CONVERSION=1
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg libsndfile1 ca-certificates build-essential \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app/web/backend
COPY web/backend/requirements.docker.txt /tmp/requirements.docker.txt
RUN python -m pip install --no-cache-dir torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cpu \
    && python -m pip install --no-cache-dir -r /tmp/requirements.docker.txt \
    && python -m pip check
COPY web/backend/ /app/web/backend/
COPY deploy/check_data.py /app/deploy/check_data.py
RUN useradd --create-home --uid 10001 asr \
    && mkdir -p /home/asr/.cache /app/dataset \
    && chown -R asr:asr /home/asr /app
USER asr
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4)" || exit 1
CMD ["sh", "-c", "python /app/deploy/check_data.py && exec python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1"]
