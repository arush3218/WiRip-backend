#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# Handle migrations with fallback strategy
echo "Running database migrations..."
python manage.py migrate --fake-initial || python manage.py migrate

# Add a success message
echo "Build completed successfully!"
