#!/bin/sh

echo "Ожидание PostgreSQL..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 1
done
echo "PostgreSQL запущен, стартуем FastAPI!"

PYTHONPATH=/app uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --workers 4