#!/usr/bin/env bash

echo "Building files..."
python3 -m pip install -r requirements.txt

# migrate the database
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

# collect static files
python3 manage.py collectstatic --noinput

# create a superuser
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@mail.com', 'admin')" | python3 manage.py shell

echo "Files built successfully!"
echo "Done!"