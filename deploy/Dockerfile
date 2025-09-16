FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ../req.txt ./ 
RUN pip install --no-cache-dir -r req.txt

RUN apt-get update && apt-get install -y postgresql-client

RUN mkdir logs
