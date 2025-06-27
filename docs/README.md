# 2025SE-Crawf.L-PassManaging

Password manager for my major

## Table of Contents
- [Building the Executable on Windows](#building-the-executable-on-windows)
- [Sprints](#sprints)
   - [First Sprint](#first-sprint)
   - [Second Sprint](#second-sprint)
   - [Third Sprint](#third-sprint)
   - [Fourth Sprint](#fourth-sprint)

## Building the Executable on Windows

1. Download the repository
2. Ensure that `bash` is installed via WSL2
   1. Install [Windows Subsytem for Linux 2](https://learn.microsoft.com/en-us/windows/wsl/install) or run the following command on PowerShell and follow the instructions from there:
      ``` powershell
      wsl --install
      ```

3. Install Python (3.13 or greater) from [python.org/downloads](https://www.python.org/downloads/).

4. Restart Windows. *Optional PowerShell command below*:
   ``` powershell
   shutdown /g /soft
   ```

5. Install the required dependencies in `bash`:
   ``` bash
   pip install pyinstaller
   pip install -r requirements.txt --upgrade
   ```

6. Run the installer script:
   <!-- note -->
   ``` bash
   ./pyinstaller.sh
   ```

# Sprints

## First Sprint

### Branch: 
[`2025SE-Crawf.L-PassManaging/testing`](https://github.com/TempeHS/2025SE-Crawf.L-PassManaging/tree/testing)

### About:

This is the first sprint as I was learning how to create local application instead a web application. This was also me trying to figure out how coding out a GUI worked and how it would appear.

## Second Sprint

### Branch:
[`2025SE-Crawf.L-PassManaging/simple`](https://github.com/TempeHS/2025SE-Crawf.L-PassManaging/tree/simple)

### About:

This second sprint was me trying to figure out `argon2id` for [Python](https://pypi.org/project/argon2-cffi/), instead of using `bcrypt` which I have used previously. This was an OOP implementation of `argon2id`, so that I could use class inheritence in Python in which I was familiar with.

## Third Sprint

### Branch: 

[`2025SE-Crawf.L-PassManaging/encrypt`](https://github.com/TempeHS/2025SE-Crawf.L-PassManaging/tree/encrypt)

### About:

This sprint was me about implementing `argon2id` with AES-256 encryption. I used `argon2id` as a key derivation function for the encryption and did testing with known files I knew the contents of (i.e. a text file).

## Fourth Sprint

### Branch: 

[`2025SE-Crawf.L-PassManaging/storage`](https://github.com/TempeHS/2025SE-Crawf.L-PassManaging/tree/storage)

### About:

Branch `storage` was the biggest sprint that I did. There was 86 commits in the [pull request #23](https://github.com/TempeHS/2025SE-Crawf.L-PassManaging/pull/23/commits). I tried to automatically encrypt a SQLite3-based template database that is located within the installation folder, if it doesn't exist then it creates a database with the same layout within the Python script.