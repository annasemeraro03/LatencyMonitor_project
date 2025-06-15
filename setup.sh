#!/bin/bash

# Rimuove lock precedente
[ -f Pipfile.lock ] && rm Pipfile.lock

# Installa i pacchetti Python dal requirements.txt
pipenv install -r requirements.txt || exit 1

# Installa le dipendenze di sistema (non Python) per WeasyPrint
sudo apt update || exit 1
sudo apt install -y libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info fonts-liberation || exit 1

# Attiva l'ambiente virtuale
exec pipenv shell
