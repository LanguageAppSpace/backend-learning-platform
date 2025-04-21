FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV DOCKER_DEFAULT_PLATFORM=linux/amd64
ENV DOCKER_BUILDKIT=1

WORKDIR /code

RUN apt-get update && \
    apt-get install -y netcat build-essential pkg-config libssl-dev libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 8080
CMD ["/bin/bash", "-c", "./django-setup.sh"]
