#!/bin/bash
# Please run this script from the root directory of the project

clear

# Ensure the repository is up-to-date
git stash && git pull 

# Install all dependencies
pip install -r requirements.txt --upgrade

# Remove the ./dist directory if it exists
if [ -d "./dist/" ]; then
    rm -rf ./dist/
fi

# Create the unified _internal directory for PyInstaller intermediates and shared libs
mkdir -p ./dist/_internal

# Build executables; .exe files go in ./dist, shared libs in ./dist/_internal
pyinstaller --clean --noconfirm --debug all --noconsole \
    --workpath ./dist/ encode.py

pyinstaller --clean --noconfirm --debug all --noconsole \
    --workpath ./dist/ decode.py