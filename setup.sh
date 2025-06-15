#!/bin/bash

# Revove precedent lock
[ -f Pipfile.lock ] && rm Pipfile.lock

# Install Python packets from requirements.txt
pipenv install -r requirements.txt || exit 1

# Install system's dependencies (not Python) for WeasyPrint
sudo apt update || exit 1
sudo apt install -y libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info fonts-liberation || exit 1

# Activate virtual environment
exec pipenv shell
