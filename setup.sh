#!/bin/bash

[ -f Pipfile.lock ] && rm Pipfile.lock

# create the Pipfile and install Django
pipenv install django==4.2.22 || exit 1

# activate shell of virtual environment
exec pipenv shell

# create a new Django project
pipenv run python manage.py runserver