FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    ADDRESS=0.0.0.0 \
    PORT=7979 \
    DEBUG=false

WORKDIR /src

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY constants/ ./constants/
COPY app/ ./app/
COPY main.py .

EXPOSE 7979

ENTRYPOINT ["/usr/local/bin/python", "./main.py"]
