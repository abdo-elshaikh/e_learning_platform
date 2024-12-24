#!/bin/bash

echo "Building files..."
python3 -m pip install -r requirements.txt

echo "Migrating database..."
# migrate the database
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

# collect static files
python3 manage.py collectstatic --noinput

# start the server
python3 manage.py runserver

echo "Done!"