#!/bin/bash

# CONFIGURATIONS
APPS="users issues experiments dashboard core analytics"

# cleanup function
cleanup() {
    echo "Stopping all processes..."
    pkill -f "manage.py startmqtt"
    exit
}

# Trap SIGINT (CTRL+C) and call cleanup
trap cleanup SIGINT

# remove old migrations and database (opzionale)
# rm -f db.sqlite3
# find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
# find . -path "*/migrations/*.pyc" -delete

# MIGRATIONS
python manage.py makemigrations $APPS       # migrations
python manage.py migrate                    # apply migrations

# create a superuser if it doesn't exist
echo "from django.contrib.auth import get_user_model;
User = get_user_model();
User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

# start MQTT listener in background
echo "Starting MQTT listener..."
python manage.py startmqtt &
MQTT_PID=$!  # Save the process ID

# run the development server
echo "Starting Django server..."
python manage.py runserver localhost:8000

# Wait for server to exit (CTRL+C will trigger the trap)
wait

# Cleanup (in case server stops for other reasons)
cleanup
