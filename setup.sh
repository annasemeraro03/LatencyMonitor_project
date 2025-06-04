#!/bin/bash

# Crea il Pipfile e installa Django
pipenv install django

# Attiva la shell dell'ambiente virtuale
exec pipenv shell
