#!/bin/bash
# Make sure to run this script from the root directory of the project

clear

# Make sure the repo is up-to-date
git stash && git pull 

# Install all dependencies
pip install -r requirements.txt --upgrade

# Remove the ./dist/main directory if it exists
if [ -d "./dist/" ]; then
	rm -rf ./dist/
fi

# Create a executable (for testing purposes)
pyinstaller --clean --noconfirm --debug all --noconsole --distpath ./dist/_internal encrypt.py
pyinstaller --clean --noconfirm --debug all --noconsole --distpath ./dist/_internal decrypt.py