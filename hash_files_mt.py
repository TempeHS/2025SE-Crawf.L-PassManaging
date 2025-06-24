import sys
import hashlib
import os
import concurrent.futures

root = sys.argv[1]

file_list = []
for dirpath, _, files in os.walk(root):
    for fname in files:
        fpath = os.path.join(dirpath, fname)
        rel = os.path.relpath(fpath, root)
        rel = rel.replace("\\", "/")
        file_list.append((fpath, rel))


def hash_file(args):
    fpath, rel = args
    hasher = hashlib.sha3_256()
    with open(fpath, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)  # Read in 1MB chunks
            if not chunk:
                break
            hasher.update(chunk)
    return f"{hasher.hexdigest()} {rel}"


with concurrent.futures.ThreadPoolExecutor() as executor:
    for result in executor.map(hash_file, file_list):
        print(result)
