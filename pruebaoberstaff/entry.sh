#!/bin/sh

echo "PostgreSQL started"

python GenKeRsa.py

python manage.py collectstatic --no-input

python manage.py migrate --no-input
exec "$@"
