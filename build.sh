#!/bin/bash

# go outside from the script when face to error
set -e

# import the local variable from .env file
export $(grep -v '^#' .env | xargs)

# install dependencies
pip install -r requirements.txt

# makemigration of database
python manage.py makemigrations
python manage.py migrate

# collect static files
python manage.py collectstatic --noinput

# creating superuser
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser(
        username='$DJANGO_SUPERUSER_USERNAME',
        email='$DJANGO_SUPERUSER_EMAIL',
        phone_number = '$DJANGO_SUPERUSER_phone',
        password='$DJANGO_SUPERUSER_PASSWORD'
    )
    print('Superuser created successfully')
else:
    print('Superuser already exists')
EOF

echo "✅ Build process completed successfully!"
