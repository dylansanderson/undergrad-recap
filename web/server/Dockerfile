FROM python:3.13-slim
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY voice/ voice/
COPY timeline.json tts.py app.py ./
RUN useradd -m narrator && chown -R narrator /app
USER narrator
ENV PYTHONUNBUFFERED=1 OMP_NUM_THREADS=2
CMD ["python", "-P", "app.py"]
