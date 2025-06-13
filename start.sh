#!/bin/bash

# remove old migrations and database
# rm -f db.sqlite3
# find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
# find . -path "*/migrations/*.pyc" -delete

# create new migrations and database
python manage.py makemigrations users
python manage.py makemigrations issues
python manage.py makemigrations experiments
python manage.py makemigrations dashboard
python manage.py makemigrations core
python manage.py makemigrations analytics

# apply migrations
python manage.py migrate

# create a superuser if it doesn't exist
echo "from django.contrib.auth import get_user_model;
User = get_user_model();
User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

# run the development server
python manage.py runserver localhost:8000 || exit 1