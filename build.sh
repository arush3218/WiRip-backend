#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# Database migration handling with better error recovery
echo "Running database migrations..."
python manage.py migrate --fake-initial || python manage.py migrate || (echo "Trying with fresh database..." && python manage.py migrate --run-syncdb)

# Add a success message
echo "Build completed successfully!"
