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

# Merge unique files from encode and decode into final, preserving subdirectory structure
mkdir -p ./dist/final

# Function to process a directory (encode or decode)
process_dir() {
    src_dir="$1"
    find "$src_dir" -type f | while read -r src_file; do
        rel_path="${src_file#$src_dir/}"
        dest_file="./dist/final/$rel_path"
        # Use Python to compute SHA3-512 hash for cross-platform compatibility
        src_hash=$(python -c "import hashlib; print(hashlib.sha3_512(open(r'$src_file','rb').read()).hexdigest())")
        if [ -f "$dest_file" ]; then
            dest_hash=$(python -c "import hashlib; print(hashlib.sha3_512(open(r'$dest_file','rb').read()).hexdigest())")
            if [ "$src_hash" != "$dest_hash" ]; then
                # Different content, copy and overwrite
                mkdir -p "$(dirname "$dest_file")"
                cp "$src_file" "$dest_file"
                echo "Overwritten: $rel_path (different content)"
            else
                echo "Skipped: $rel_path (identical file exists)"
            fi
        else
            # File does not exist, copy and preserve subdirectories
            mkdir -p "$(dirname "$dest_file")"
            cp "$src_file" "$dest_file"
            echo "Copied: $rel_path (new file)"
        fi
    done
}

process_dir ./dist/encode
process_dir ./dist/decode

echo "Merged unique files from ./dist/encode and ./dist/decode into ./dist/final (duplicates removed, subdirectories preserved)"