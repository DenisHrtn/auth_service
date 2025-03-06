#!/bin/bash

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done

while ! nc -z redis 6379; do
  echo "Ожидание запуска Redis..."
  sleep 2
done

echo "Starting Celery..."
exec poetry run celery -A app.infra.celery.celery_app.app worker --loglevel=info