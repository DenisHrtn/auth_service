#!/bin/bash

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done

echo "Starting Celery..."
exec poetry run celery -A app.infra.celery.celery_app.app worker --loglevel=info