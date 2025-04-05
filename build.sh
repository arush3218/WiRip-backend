#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# Handle migrations with fallback strategy
echo "Running database migrations..."
python manage.py migrate --fake-initial || python manage.py migrate

# Create a superuser non-interactively if it doesn't exist
echo "Ensuring admin user exists..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wirip_api.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
    os.environ.get('DJANGO_ADMIN_USERNAME', 'admin'),
    os.environ.get('DJANGO_ADMIN_EMAIL', 'admin@example.com'),
    os.environ.get('DJANGO_ADMIN_PASSWORD', '123455')
)
else:
    print('Superuser already exists.')
"

# Add a success message
echo "Build completed successfully!"
