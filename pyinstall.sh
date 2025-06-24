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

# Helper: Hash all files in a directory, outputting "<hash> <relative_path>"
hash_files_py="
import sys, hashlib, os
root = sys.argv[1]
for dirpath, _, files in os.walk(root):
    for fname in files:
        fpath = os.path.join(dirpath, fname)
        rel = os.path.relpath(fpath, root)
        rel = rel.replace('\\\\', '/')  # Always use forward slashes
        with open(fpath, 'rb') as f:
            h = hashlib.sha3_512(f.read()).hexdigest()
        print(f'{h} {rel}')
"

# Hash and collect all files from encode and decode
mkdir -p ./dist/final

python -c "$hash_files_py" ./dist/encode > /tmp/encode_hashes.txt
python -c "$hash_files_py" ./dist/decode > /tmp/decode_hashes.txt

# Merge hashes, keeping track of what has been copied
cat /tmp/encode_hashes.txt /tmp/decode_hashes.txt | while read hash relpath; do
    dest="./dist/final/$relpath"
    src=""
    if [ -f "./dist/encode/$relpath" ]; then
        src="./dist/encode/$relpath"
    elif [ -f "./dist/decode/$relpath" ]; then
        src="./dist/decode/$relpath"
    fi
    # Only copy if this hash/relpath combo hasn't been seen yet
    if [ ! -f "$dest" ]; then
        if [ -n "$src" ] && [ -f "$src" ]; then
            mkdir -p "$(dirname "$dest")"
            cp "$src" "$dest"
            echo "Copied: $relpath (new file)"
        else
            echo "Skipped: $relpath (source file not found)"
        fi
    else
        # Compare hash of existing file
        dest_hash=$(python -c "import hashlib; print(hashlib.sha3_512(open(r'$dest','rb').read()).hexdigest())")
        if [ "$dest_hash" != "$hash" ]; then
            cp "$src" "$dest"
            echo "Overwritten: $relpath (different content)"
        else
            echo "Skipped: $relpath (identical file exists)"
        fi
    fi
done

echo "Merged unique files from ./dist/encode and ./dist/decode into ./dist/final (duplicates removed, subdirectories preserved)"