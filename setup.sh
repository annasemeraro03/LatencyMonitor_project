#!/bin/bash

# check if Pipfile.lock exists and remove it if it does
[ -f Pipfile.lock ] && rm Pipfile.lock

# create the Pipfile and install libraries
pipenv install -r requirements.txt || exit 1

# activate shell of virtual environment
exec pipenv shell