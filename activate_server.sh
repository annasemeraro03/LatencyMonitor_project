# makemigrations 
python manage.py makemigrations users
python manage.py makemigrations issues
python manage.py makemigrations experiments
python manage.py makemigrations dashboard
python manage.py makemigrations core

python manage.py migrate

# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser

#run server
python manage.py runserver localhost:8000 || exit 1