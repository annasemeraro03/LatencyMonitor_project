#!/bin/bash

# Flag for installing dependencies
INSTALL_DEPS=false

# Revove precedent lock
echo -e "\033[1;32m>> Removing Pipfile.lock if present \033[0m"
[ -f Pipfile.lock ] && rm Pipfile.lock

# Install Python packets from requirements.txt
echo -e "\033[1;32m>> Installing requirements from file requirements.txt\033[0m"
pipenv install -r requirements.txt || exit 1

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -d|--deps) INSTALL_DEPS=true ;;
        *) echo -e "\033[1;32m>> Ignored unrecognized argument: $1\033[0m" ;;
    esac
    shift
done

# Install system's dependencies (not Python) for WeasyPrint
if [ "$INSTALL_DEPS" = true ]; then
    echo -e "\033[1;32m>> Installing system dependencies for WeasyPrint\033[0m"
    sudo apt update || exit 1
    sudo apt install -y libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
        libgdk-pixbuf2.0-0 libffi-dev shared-mime-info fonts-liberation || exit 1
fi

# Activate virtual environment
echo -e "\033[1;32m>> Executing virtual environment \033[0m" 
exec pipenv shell
