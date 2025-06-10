#!/bin/bash

# check if Pipfile.lock exists and remove it if it does
[ -f Pipfile.lock ] && rm Pipfile.lock

# create the Pipfile and install libraries
pipenv install -r requirements.txt || exit 1

# pipenv install django==4.2.22 || exit 1
# pipenv install djangorestframework || exit 1
# pipenv install pillow || exit 1
# pipenv install plotly || exit 1
# pipenv install weasyprint || exit 1

# activate shell of virtual environment
exec pipenv shell