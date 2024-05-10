FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

