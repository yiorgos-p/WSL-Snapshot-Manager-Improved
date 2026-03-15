# WSL Snapshot Manager

import subprocess
import os
import json
import datetime
import time
import threading
import shutil
import gzip
import re

from termcolor import colored

CONFIG_FILE = os.path.expanduser("~/.wsl_snapshot_config.json")

DEFAULT_CONFIG = {
    "backup_dir": os.path.expanduser("~/wsl_backups")
}

spinner_running = False

def spinner():
    global spinner_running
    while spinner_running:
        for cursor in '|/-\\':
            print(cursor, end='\r', flush=True)
            time.sleep(0.1)

def start_spinner():
    global spinner_running
    spinner_running = True
    threading.Thread(target=spinner, daemon=True).start()

def stop_spinner():
    global spinner_running
    spinner_running = False
    print(' ', end='\r', flush=True)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)


def save_backup_metadata(backup_path, distro_name, wsl_version, notes=""):
    """Save metadata for a backup"""
    metadata = {
        "original_distro": distro_name,
        "created_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "wsl_version": wsl_version,
        "notes": notes,
        "created_by": "wsl_snapshot_manager"
    }
    
    # Add file sizes
    if os.path.exists(backup_path):
        compressed_size = os.path.getsize(backup_path)
        metadata["size_compressed"] = compressed_size
        metadata["size_compressed_mb"] = round(compressed_size / (1024 * 1024), 2)
    
    metadata_path = backup_path + ".meta.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)


def load_backup_metadata(backup_path):
    """Load metadata for a backup"""
    metadata_path = backup_path + ".meta.json"
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            return json.load(f)
    return None


def get_backup_info(backup_dir, backup_filename):
    """Get comprehensive info about a backup"""
    backup_path = os.path.normpath(os.path.join(backup_dir, backup_filename))
    info = {
        "filename": backup_filename,
        "path": backup_path,
        "exists": os.path.exists(backup_path)
    }
    
    if info["exists"]:
        info["size_mb"] = round(os.path.getsize(backup_path) / (1024 * 1024), 2)
        info["modified_date"] = datetime.datetime.fromtimestamp(
            os.path.getmtime(backup_path)
        ).strftime("%Y-%m-%d %H:%M:%S")
    
    # Load metadata if available
    metadata = load_backup_metadata(backup_path)
    if metadata:
        info["metadata"] = metadata
    
    return info


def list_distros():
    result = subprocess.run(["wsl", "--list", "--verbose"], capture_output=True)
    output = result.stdout.decode('utf-16').strip()
    lines = output.splitlines()

    distros = []
    
    for line in lines[1:]:
        match = re.match(r'([* ]?)\s*([^\s]+)\s+([^\s]+)\s+(\d+)', line.strip())
        if match:
            is_default = match.group(1) == '*'
            name = match.group(2)
            state = match.group(3)
            version = int(match.group(4))
            
            distros.append([
                name,
                state,
                version,
                is_default
            ])

    return distros




def list_backups(backup_dir):
    backup_dir = os.path.normpath(backup_dir)
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    backups = [f for f in os.listdir(backup_dir) if f.endswith('.tar.gz')]
    return backups

def export_distro():
    config = load_config()
    backup_dir = os.path.normpath(config['backup_dir'])
    
    # Ensure backup directory exists
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    distros = list_distros()
    if not distros:
        print(colored("No distros available to export.", "red"))
        return

    print("\nAvailable distros to export:")
    for idx, (distro, state, version, is_default) in enumerate(distros, 1):
        distro_colored = colored(f"{distro:20}", "yellow")
        state_colored = colored(f"{state:15}", "magenta")
        version_colored = colored(f"(WSL {version:5})", "blue")
        label = f"{distro_colored}{state_colored}{version_colored}"
        if is_default:
            label += colored(" [default]", "green")
        print(f"{colored(str(idx) + '.', 'cyan')} {label}")

    choice = int(input("Select a distro to export: ")) - 1
    selected_distro, state, version, is_default = distros[choice]

    # Ask for optional notes
    notes = input("Add notes for this backup (optional, press Enter to skip): ").strip()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    backup_file = os.path.normpath(os.path.join(backup_dir, f"{selected_distro}-{timestamp}.tar"))
    compressed_backup_file = backup_file + ".gz"

    print(colored(f"Exporting {selected_distro} to {compressed_backup_file}...", "cyan"))
    start_spinner()
    subprocess.run(["wsl", "--export", selected_distro, backup_file])
    stop_spinner()

    print(colored("Compressing backup...", "cyan"))
    with open(backup_file, 'rb') as f_in, gzip.open(compressed_backup_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    os.remove(backup_file)

    # Save metadata
    save_backup_metadata(compressed_backup_file, selected_distro, version, notes)

    print(colored("Export and compression complete! ✅", "green"))


def import_distro():
    config = load_config()
    backup_dir = os.path.normpath(config['backup_dir'])

    backups = list_backups(backup_dir)
    if not backups:
        print(colored("No backups available to import.", "red"))
        return

    print("Available backups to import:")
    for idx, backup in enumerate(backups, 1):
        print(f"{idx}. {backup}")

    choice = int(input("Select a backup to import: ")) - 1
    selected_backup = backups[choice]

    new_distro_name = input("Enter a name for the new distro: ")
    default_install_location = os.path.normpath(os.path.expanduser(f"~/wsl_installs/{new_distro_name}"))
    install_location_input = input(f"Enter the install location (default: {default_install_location}): ")
    
    # Strip quotes and normalize install location
    if install_location_input:
        install_location = os.path.normpath(os.path.abspath(os.path.expanduser(install_location_input.strip().strip('"').strip("'"))))
    else:
        install_location = default_install_location
    
    # Ensure install directory exists
    if not os.path.exists(install_location):
        os.makedirs(install_location)

    compressed_backup_path = os.path.normpath(os.path.join(backup_dir, selected_backup))
    extracted_backup_path = compressed_backup_path[:-3]  # remove .gz

    print(colored("Decompressing backup...", "cyan"))
    start_spinner()
    with gzip.open(compressed_backup_path, 'rb') as f_in, open(extracted_backup_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    stop_spinner()

    print(colored(f"Importing {new_distro_name} from {extracted_backup_path} into {install_location}...", "cyan"))
    start_spinner()
    subprocess.run(["wsl", "--import", new_distro_name, install_location, extracted_backup_path])
    stop_spinner()

    os.remove(extracted_backup_path)

    print(colored("Import complete! ✅", "green"))

def export_all_distros():
    """Export all or selected distros at once"""
    config = load_config()
    backup_dir = os.path.normpath(config['backup_dir'])
    
    # Ensure backup directory exists
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    distros = list_distros()
    if not distros:
        print(colored("No distros available to export.", "red"))
        return

    print("\nAvailable distros:")
    for idx, (distro, state, version, is_default) in enumerate(distros, 1):
        distro_colored = colored(f"{distro:20}", "yellow")
        state_colored = colored(f"{state:15}", "magenta")
        version_colored = colored(f"(WSL {version:5})", "blue")
        label = f"{distro_colored}{state_colored}{version_colored}"
        if is_default:
            label += colored(" [default]", "green")
        print(f"{colored(str(idx) + '.', 'cyan')} {label}")

    print("\nOptions:")
    print("1. Export ALL distros")
    print("2. Select specific distros to export")
    print("3. Cancel")
    
    choice = input("Select an option: ")
    
    selected_distros = []
    
    if choice == '1':
        selected_distros = distros
    elif choice == '2':
        selection = input("Enter distro numbers separated by commas (e.g., 1,3,4): ")
        indices = [int(i.strip()) - 1 for i in selection.split(',')]
        selected_distros = [distros[i] for i in indices if 0 <= i < len(distros)]
    else:
        print(colored("Cancelled.", "yellow"))
        return
    
    if not selected_distros:
        print(colored("No distros selected.", "red"))
        return
    
    # Ask for optional notes for all backups
    notes = input("Add notes for these backups (optional, press Enter to skip): ").strip()
    
    print(colored(f"\nExporting {len(selected_distros)} distro(s)...", "cyan"))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    
    for idx, (distro_name, state, version, is_default) in enumerate(selected_distros, 1):
        print(colored(f"\n[{idx}/{len(selected_distros)}] Exporting {distro_name}...", "yellow"))
        
        backup_file = os.path.normpath(os.path.join(backup_dir, f"{distro_name}-{timestamp}.tar"))
        compressed_backup_file = backup_file + ".gz"
        
        start_spinner()
        subprocess.run(["wsl", "--export", distro_name, backup_file])
        stop_spinner()
        
        print(colored("Compressing...", "cyan"))
        with open(backup_file, 'rb') as f_in, gzip.open(compressed_backup_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        os.remove(backup_file)
        
        # Save metadata
        save_backup_metadata(compressed_backup_file, distro_name, version, notes)
    
    print(colored(f"\n✅ Successfully exported {len(selected_distros)} distro(s)!", "green"))


def clone_distro():
    """Clone a distro by exporting and immediately importing with a new name"""
    config = load_config()
    backup_dir = os.path.normpath(config['backup_dir'])
    
    distros = list_distros()
    if not distros:
        print(colored("No distros available to clone.", "red"))
        return

    print("\nAvailable distros to clone:")
    for idx, (distro, state, version, is_default) in enumerate(distros, 1):
        distro_colored = colored(f"{distro:20}", "yellow")
        state_colored = colored(f"{state:15}", "magenta")
        version_colored = colored(f"(WSL {version:5})", "blue")
        label = f"{distro_colored}{state_colored}{version_colored}"
        if is_default:
            label += colored(" [default]", "green")
        print(f"{colored(str(idx) + '.', 'cyan')} {label}")

    choice = int(input("Select a distro to clone: ")) - 1
    source_distro, state, version, is_default = distros[choice]
    
    new_distro_name = input(f"Enter a name for the cloned distro: ").strip()
    if not new_distro_name:
        print(colored("Clone cancelled - no name provided.", "red"))
        return
    
    # Check if name already exists
    existing_names = [d[0] for d in distros]
    if new_distro_name in existing_names:
        print(colored(f"Error: A distro named '{new_distro_name}' already exists!", "red"))
        return
    
    default_install_location = os.path.normpath(os.path.expanduser(f"~/wsl_installs/{new_distro_name}"))
    install_location_input = input(f"Install location (default: {default_install_location}): ")
    
    if install_location_input:
        install_location = os.path.normpath(os.path.abspath(
            os.path.expanduser(install_location_input.strip().strip('"').strip("'"))
        ))
    else:
        install_location = default_install_location
    
    # Ensure install directory exists
    if not os.path.exists(install_location):
        os.makedirs(install_location)
    
    # Use temp directory for intermediate export
    temp_export = os.path.join(backup_dir, f"_temp_clone_{source_distro}.tar")
    
    print(colored(f"\nCloning {source_distro} → {new_distro_name}", "cyan"))
    print(colored(f"Step 1/2: Exporting {source_distro}...", "yellow"))
    start_spinner()
    subprocess.run(["wsl", "--export", source_distro, temp_export])
    stop_spinner()
    
    print(colored(f"Step 2/2: Importing as {new_distro_name}...", "yellow"))
    start_spinner()
    subprocess.run(["wsl", "--import", new_distro_name, install_location, temp_export])
    stop_spinner()
    
    # Clean up temp file
    if os.path.exists(temp_export):
        os.remove(temp_export)
    
    print(colored(f"✅ Successfully cloned {source_distro} to {new_distro_name}!", "green"))


def manage_backups():
    """Manage existing backups - view, delete, rename"""
    config = load_config()
    backup_dir = os.path.normpath(config['backup_dir'])
    
    while True:
        backups = list_backups(backup_dir)
        
        print(colored("\n=== Backup Management ===", "yellow"))
        print("1. List all backups")
        print("2. View backup details")
        print("3. Delete a backup")
        print("4. Rename a backup")
        print("5. Back to main menu")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            # List all backups
            if not backups:
                print(colored("No backups found.", "red"))
                continue
            
            print(colored(f"\n=== Found {len(backups)} backup(s) ===", "cyan"))
            for idx, backup in enumerate(backups, 1):
                info = get_backup_info(backup_dir, backup)
                print(f"\n{colored(str(idx) + '.', 'cyan')} {colored(backup, 'yellow')}")
                print(f"   Size: {info.get('size_mb', '?')} MB")
                print(f"   Modified: {info.get('modified_date', 'Unknown')}")
                
                if 'metadata' in info:
                    meta = info['metadata']
                    print(f"   Original: {meta.get('original_distro', 'Unknown')}")
                    print(f"   WSL Version: {meta.get('wsl_version', 'Unknown')}")
                    if meta.get('notes'):
                        print(f"   Notes: {colored(meta['notes'], 'magenta')}")
        
        elif choice == '2':
            # View backup details
            if not backups:
                print(colored("No backups found.", "red"))
                continue
            
            print("\nAvailable backups:")
            for idx, backup in enumerate(backups, 1):
                print(f"{idx}. {backup}")
            
            try:
                selection = int(input("Select a backup to view: ")) - 1
                if 0 <= selection < len(backups):
                    info = get_backup_info(backup_dir, backups[selection])
                    print(colored(f"\n=== Details for {backups[selection]} ===", "cyan"))
                    print(f"Path: {info['path']}")
                    print(f"Size: {info.get('size_mb', '?')} MB")
                    print(f"Modified: {info.get('modified_date', 'Unknown')}")
                    
                    if 'metadata' in info:
                        meta = info['metadata']
                        print(colored("\nMetadata:", "yellow"))
                        print(f"  Original Distro: {meta.get('original_distro', 'Unknown')}")
                        print(f"  Created: {meta.get('created_date', 'Unknown')}")
                        print(f"  WSL Version: {meta.get('wsl_version', 'Unknown')}")
                        print(f"  Compressed Size: {meta.get('size_compressed_mb', '?')} MB")
                        if meta.get('notes'):
                            print(f"  Notes: {colored(meta['notes'], 'magenta')}")
                    else:
                        print(colored("No metadata available for this backup.", "yellow"))
            except (ValueError, IndexError):
                print(colored("Invalid selection.", "red"))
        
        elif choice == '3':
            # Delete a backup
            if not backups:
                print(colored("No backups found.", "red"))
                continue
            
            print("\nAvailable backups:")
            for idx, backup in enumerate(backups, 1):
                info = get_backup_info(backup_dir, backup)
                print(f"{idx}. {backup} ({info.get('size_mb', '?')} MB)")
            
            try:
                selection = int(input("Select a backup to DELETE: ")) - 1
                if 0 <= selection < len(backups):
                    confirm = input(colored(f"Are you sure you want to delete '{backups[selection]}'? (yes/no): ", "red"))
                    if confirm.lower() in ['yes', 'y']:
                        backup_path = os.path.join(backup_dir, backups[selection])
                        metadata_path = backup_path + ".meta.json"
                        
                        os.remove(backup_path)
                        if os.path.exists(metadata_path):
                            os.remove(metadata_path)
                        
                        print(colored(f"✅ Deleted {backups[selection]}", "green"))
                    else:
                        print(colored("Deletion cancelled.", "yellow"))
            except (ValueError, IndexError):
                print(colored("Invalid selection.", "red"))
        
        elif choice == '4':
            # Rename a backup
            if not backups:
                print(colored("No backups found.", "red"))
                continue
            
            print("\nAvailable backups:")
            for idx, backup in enumerate(backups, 1):
                print(f"{idx}. {backup}")
            
            try:
                selection = int(input("Select a backup to rename: ")) - 1
                if 0 <= selection < len(backups):
                    old_name = backups[selection]
                    new_name = input(f"Enter new name (current: {old_name}): ").strip()
                    
                    if not new_name.endswith('.tar.gz'):
                        new_name += '.tar.gz'
                    
                    old_path = os.path.join(backup_dir, old_name)
                    new_path = os.path.join(backup_dir, new_name)
                    old_meta = old_path + ".meta.json"
                    new_meta = new_path + ".meta.json"
                    
                    if os.path.exists(new_path):
                        print(colored(f"Error: {new_name} already exists!", "red"))
                    else:
                        os.rename(old_path, new_path)
                        if os.path.exists(old_meta):
                            os.rename(old_meta, new_meta)
                        print(colored(f"✅ Renamed {old_name} → {new_name}", "green"))
            except (ValueError, IndexError):
                print(colored("Invalid selection.", "red"))
        
        elif choice == '5':
            break
        else:
            print(colored("Invalid choice.", "red"))


def set_backup_dir():
    new_dir = input("Enter new backup directory path: ")
    # Strip quotes and whitespace
    new_dir = new_dir.strip().strip('"').strip("'")
    # Expand user home directory and normalize path
    new_dir = os.path.normpath(os.path.abspath(os.path.expanduser(new_dir)))
    # Ensure the directory exists
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    config = load_config()
    config['backup_dir'] = new_dir
    save_config(config)
    print(colored(f"Backup directory set to {new_dir}", "green"))

def main_menu():
    while True:
        config = load_config()
        print(colored("\n=== WSL Snapshot Manager ===", "yellow"))
        print("---\nBackup directory: " + colored(config['backup_dir'], "green") + "\n---\n")
        print("1. Export a WSL distro")
        print("2. Export all distros")
        print("3. Clone a distro")
        print("4. Import a WSL distro")
        print("5. Manage backups")
        print("6. Set backup directory")
        print("7. Exit")

        choice = input("\nSelect an option: ")

        if choice == '1':
            export_distro()
        elif choice == '2':
            export_all_distros()
        elif choice == '3':
            clone_distro()
        elif choice == '4':
            import_distro()
        elif choice == '5':
            manage_backups()
        elif choice == '6':
            set_backup_dir()
        elif choice == '7':
            print(colored("Goodbye! 👋", "yellow"))
            break
        else:
            print(colored("Invalid choice. Please select again.", "red"))

if __name__ == "__main__":
    main_menu()
