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

# Hash all files in final (if any)
python -c "$hash_files_py" ./dist/final > /tmp/final_hashes.txt

# Build a lookup table of relpath -> hash for final
declare -A final_hashes
while read -r hash relpath; do
    final_hashes["$relpath"]="$hash"
done < <(awk 'NF==2' /tmp/final_hashes.txt)

# Merge hashes, keeping track of what has been copied
awk 'NF==2' /tmp/encode_hashes.txt /tmp/decode_hashes.txt | while read -r hash relpath; do
    echo "[DEBUG] Processing line: hash='$hash', relpath='$relpath'"
    relpath="$(echo "$relpath" | xargs)"
    if [ -z "$hash" ] || [ -z "$relpath" ]; then
        echo "[DEBUG] Skipped: malformed line (hash='$hash', relpath='$relpath')"
        continue
    fi

    dest="./dist/final/$relpath"
    src=""
    if [ -f "./dist/encode/$relpath" ]; then
        src="./dist/encode/$relpath"
        echo "[DEBUG] Found in encode: $src"
    elif [ -f "./dist/decode/$relpath" ]; then
        src="./dist/decode/$relpath"
        echo "[DEBUG] Found in decode: $src"
    else
        echo "[DEBUG] Source file not found for: $relpath"
    fi

    if [ -n "$src" ] && [ -f "$src" ]; then
        mkdir -p "$(dirname "$dest")"
        final_hash="${final_hashes[$relpath]}"
        if [ -z "$final_hash" ]; then
            cp "$src" "$dest"
            echo "Copied: $relpath (new file)"
            final_hashes["$relpath"]="$hash"
        else
            echo "[DEBUG] Comparing dest hash: $final_hash with source hash: $hash for $relpath"
            if [ "$final_hash" != "$hash" ]; then
                cp "$src" "$dest"
                echo "Overwritten: $relpath (different content)"
                final_hashes["$relpath"]="$hash"
            else
                echo "Skipped: $relpath (identical file exists)"
            fi
        fi
    else
        echo "Skipped: $relpath (source file not found)"
    fi
    echo "[DEBUG] Finished processing: $relpath"
done

echo "Merged unique files from ./dist/encode and ./dist/decode into ./dist/final (duplicates removed, subdirectories preserved)"