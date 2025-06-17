#!/bin/bash

# CONFIGURATIONS
APPS="users issues experiments dashboard core analytics"
REMOVE_DATABASE=false
REMOVE_ALL_MIGRATIONS=false

# cleanup function
cleanup() {
    echo -e "\033[1;32m>> Stopping all processes... $1\033[0m"
    pkill -f "manage.py startmqtt"
    exit
}

# Trap SIGINT (CTRL+C) and call cleanup
trap cleanup SIGINT

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -rd|--remove-database) REMOVE_DATABASE=true ;;
        -rm|--remove-migrations) REMOVE_ALL_MIGRATIONS=true ;;
        *) echo -e "\033[1;32m>> Ignored unrecognized argument: $1\033[0m" ;;
    esac
    shift
done

if [ "$REMOCE_DATABASE" = true ]; then
    echo -e "\033[1;32m>> Removing database \033[0m"
    rm -f db.sqlite3
fi

# remove old migrations and database 
if [ "$REMOVE_ALL_MIGRATIONS" = true ]; then
    echo -e "\033[1;32m>> Removing old migrations \033[0m"
    find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
    find . -path "*/migrations/*.pyc" -delete
fi

# MIGRATIONS
echo -e "\033[1;32m>> Making new migrations \033[0m"
# migrations
python manage.py makemigrations users   
python manage.py makemigrations analytics  
python manage.py makemigrations experiments       
python manage.py makemigrations dashboard  
python manage.py makemigrations core   
python manage.py makemigrations issues      
python manage.py migrate                    # apply migrations

# create a superuser if it doesn't exist
echo "from django.contrib.auth import get_user_model;
User = get_user_model();
User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

# start MQTT listener in background
echo -e "\033[1;32m>> Starting MQTT listener...\033[0m"
python manage.py startmqtt &
MQTT_PID=$!  # Save the process ID

# run the development server
echo -e "\033[1;32m>> Starting Django server...\033[0m"
python manage.py runserver localhost:8000

# Wait for server to exit (CTRL+C will trigger the trap)
wait

# Cleanup (in case server stops for other reasons)
cleanup
