#!/bin/sh
set -e

cd /code/app

# Prepare runtime dirs
mkdir -p logs media staticfiles

# DB migrations
python manage.py migrate --noinput

# Collect static
python manage.py collectstatic --noinput || true

# Start server
python manage.py runserver 0.0.0.0:8000
