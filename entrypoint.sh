#!/bin/sh

echo "Ожидание PostgreSQL..."
while ! nc -z $DB_CONFIG__postgres_host $DB_CONFIG__postgres_port; do
    sleep 1
done
echo "PostgreSQL запущен, стартуем FastAPI!"

echo "Создаем миграции..."
cd /app
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
cd src

PYTHONPATH=/app uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload