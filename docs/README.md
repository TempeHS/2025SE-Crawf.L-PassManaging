# 2025SE-Crawf.L-PassManaging

Password manager for my major

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