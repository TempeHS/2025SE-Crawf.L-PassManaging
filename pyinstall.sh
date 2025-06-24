#!/bin/bash
# Please run this script from the root directory of the project

clear

# Ensure the repository is up-to-date
git stash && git pull 

# Install all dependencies
pip install -r requirements.txt --upgrade

# Remove the ./dist directory and all contents
if [ -d "./dist/" ]; then
	echo "Removing existing ./dist directory..."
	rm -rf ./dist/
else
	echo "No existing ./dist directory found."
fi

# Build executables; .exe files go in ./dist
pyinstaller --clean --noconfirm --debug all --noconsole --specpath ./build encode.py

pyinstaller --clean --noconfirm --debug all --noconsole --specpath ./build decode.py

# Merge files from encode and decode into final, preserving subdirectory structure, skipping files that already exist
for srcdir in ./dist/encode ./dist/decode; do
    if [ -d "$srcdir" ]; then
        find "$srcdir" -type f | while read -r src; do
            relpath="${src#$srcdir/}"
            dest="./dist/final/$relpath"
            if [ -f "$dest" ]; then
                echo "Skipped: $relpath (already exists in final)"
            else
                mkdir -p "$(dirname "$dest")"
                start_time=$(date +%s.%N)
                cp "$src" "$dest"
                end_time=$(date +%s.%N)
                duration=$(echo "$end_time - $start_time" | bc)
                echo "Copied: $relpath [COPY TIMESTAMP] $(date '+%Y-%m-%d %H:%M:%S') duration: ${duration}s"
            fi
        done
    else
        echo "Source directory not found: $srcdir"
    fi
done

echo "Merged files from ./dist/encode and ./dist/decode into ./dist/final (skipped files that already exist, subdirectories preserved)"