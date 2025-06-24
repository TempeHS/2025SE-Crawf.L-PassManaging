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
pyinstaller --clean --noconfirm --debug all --noconsole \
	--specpath ./build encode.py

pyinstaller --clean --noconfirm --debug all --noconsole \
	--specpath ./build decode.py

# Merge the ./dist/encode and ./dist/decode folders into ./dist/final
mkdir -p ./dist/final

# # Copy unique files from encode
# if [ -d "./dist/encode" ]; then
# 	for file in ./dist/encode/*; do
# 		basefile=$(basename "$file")
# 		if [ ! -e "./dist/final/$basefile" ]; then
# 			cp -r "$file" ./dist/final/
# 		fi
# 	done
# fi

# # Copy unique files from decode
# if [ -d "./dist/decode" ]; then
# 	for file in ./dist/decode/*; do
# 		basefile=$(basename "$file")
# 		if [ ! -e "./dist/final/$basefile" ]; then
# 			cp -r "$file" ./dist/final/
# 		fi
# 	done
# fi

# use sha3-512 to compare files and copy unique files
# if there are files with the same name, but different content, they will be copied
if [ -d "./dist/encode" ]; then
	for file in ./dist/encode/*; do
		basefile=$(basename "$file")
		if [ ! -e "./dist/final/$basefile" ]; then
			cp -r "$file" ./dist/final/
		else
			# Compare files using sha3-512
			if ! sha3sum "$file" | cut -d ' ' -f 1 | grep -q "$(sha3sum "./dist/final/$basefile" | cut -d ' ' -f 1)"; then
				cp -r "$file" "./dist/final/$basefile"
			fi
		fi
	done
fi

if [ -d "./dist/decode" ]; then
	for file in ./dist/decode/*; do
		basefile=$(basename "$file")
		if [ ! -e "./dist/final/$basefile" ]; then
			cp -r "$file" ./dist/final/
		else
			# Compare files using sha3-512
			if ! sha3sum "$file" | cut -d ' ' -f 1 | grep -q "$(sha3sum "./dist/final/$basefile" | cut -d ' ' -f 1)"; then
				cp -r "$file" "./dist/final/$basefile"
			fi
		fi
	done
fi

echo "Merged ./dist/encode and ./dist/decode into ./dist/final (duplicates removed)"