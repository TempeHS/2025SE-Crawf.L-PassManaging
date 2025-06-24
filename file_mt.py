import sys
import os
import shutil
import time
import concurrent.futures

# Set source and destination directories
src_dirs = ["./dist/encode", "./dist/decode"]
dest_root = "./dist/final"

# Collect all files to copy (preserving subdirectory structure)
file_jobs = []
copied = set()
for src_dir in src_dirs:
    if not os.path.isdir(src_dir):
        print(f"Source directory not found: {src_dir}")
        continue
    for dirpath, _, files in os.walk(src_dir):
        for fname in files:
            src = os.path.join(dirpath, fname)
            relpath = os.path.relpath(src, src_dir)
            dest = os.path.join(dest_root, relpath)
            if dest in copied or os.path.isfile(dest):
                print(f"Skipped: {relpath} (already exists in final)")
                continue
            file_jobs.append((src, dest, relpath))
            copied.add(dest)


def copy_file(job):
    src, dest, relpath = job
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    start = time.time()
    shutil.copy2(src, dest)
    end = time.time()
    print(
        f"Copied: {relpath} [COPY TIMESTAMP] {time.strftime('%Y-%m-%d %H:%M:%S')} duration: {end-start:.4f}s"
    )


start_all = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    executor.map(copy_file, file_jobs)
end_all = time.time()

print(
    f"Merged files from ./dist/encode and ./dist/decode into ./dist/final (skipped files that already exist, subdirectories preserved)"
)
print(f"Total copy duration: {end_all-start_all:.2f} seconds")
