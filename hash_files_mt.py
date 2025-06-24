import sys
import hashlib
import os
import concurrent.futures

root = sys.argv[1]

# Collect all files to hash
file_list = []
for dirpath, _, files in os.walk(root):
    for fname in files:
        fpath = os.path.join(dirpath, fname)
        rel = os.path.relpath(fpath, root)
        rel = rel.replace('\\', '/')  # Always use forward slashes
        file_list.append((fpath, rel))

def hash_file(args):
    fpath, rel = args
    with open(fpath, 'rb') as f:
        h = hashlib.sha3_512(f.read()).hexdigest()
    return f'{h} {rel}'

with concurrent.futures.ThreadPoolExecutor() as executor:
    for result in executor.map(hash_file, file_list):
        print(result)
