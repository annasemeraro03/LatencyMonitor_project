# makemigrations 
python manage.py makemigrations users
python manage.py makemigrations issues
python manage.py makemigrations experiments
python manage.py makemigrations dashboard
python manage.py makemigrations core

# migrate
python manage.py migrate

# create superuser if needed
# python manage.py createsuperuser
# user: admin, password: admin

#run server
python manage.py runserver localhost:8000 || exit 1