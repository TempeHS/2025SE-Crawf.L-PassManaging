#!/bin/bash
# Please run this script from the root directory of the project

clear

# Ensure the repository is up-to-date
git stash && git pull 

# Install all dependencies
pip install -r requirements.txt --upgrade

# Remove the ./dist directory and all contents
if [ -d "./dist/final/" ]; then
	echo "Removing existing ./dist directory..."
	rm -rf ./dist/final/
else
	echo "No existing ./dist/final/ directory found."
fi

# Build executables using PyInstaller
pyinstaller --clean --noconfirm --debug all --noconsole --specpath ./build encode.py

pyinstaller --clean --noconfirm --debug all --noconsole --specpath ./build decode.py

# Merge files using cross-platform Python script
python ./building/hash_file_mt.py