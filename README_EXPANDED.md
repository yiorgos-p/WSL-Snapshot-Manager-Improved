# 🐧 WSL Snapshot Manager - Expanded Version

This is the **expanded version** with new features for power users.

**Looking for the basic version?** → [README_BASIC.md](./README_BASIC.md)  
**Back to main page** → [README.md](./README.md)

---

**WSL Snapshot Manager** is a powerful, interactive CLI tool to **backup**, **restore**, and **manage** your WSL (Windows Subsystem for Linux) distros with ease.

## ✨ Features

### Core Functionality
- 📦 **Export WSL distros** into compressed `.tar.gz` snapshots with metadata
- 🛠 **Import snapshots** back into WSL with custom names and locations
- 🔄 **Clone distros** instantly without manual export/import workflow
- 📊 **Export all distros** at once - bulk backup in one command
- 🗂 **Manage backups** - list, view details, delete, and rename backups

### Advanced Features
- 📝 **Backup metadata** - store notes, dates, WSL version, and size info with each backup
- 📂 Customizable backup directory with automatic creation
- 🎨 Colored output for better UX
- 🔄 Progress spinner during operations
- ⚡ Auto-detects WSL1 or WSL2 versions

---

## 🛠 Requirements

- **Python 3.7+**
- **Windows 10/11** with WSL installed
- Python packages listed in `requirements.txt`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/ekinakkaya/wsl-snapshot-manager.git
cd wsl-snapshot-manager
```

Install dependencies & run the tool:

```bash
pip install -r requirements.txt
python wsl_snapshot_manager_expanded.py
```

---

## 📋 Usage

### Main Menu

```
=== WSL Snapshot Manager ===
Backup directory: C:\Users\YourName\wsl_backups

1. Export a WSL distro
2. Export all distros
3. Clone a distro
4. Import a WSL distro
5. Manage backups
6. Set backup directory
7. Exit
```

### 1. Export a Distro
- Select an installed WSL distro
- Add optional notes (e.g., "Before kernel upgrade")
- Creates compressed backup with metadata

### 2. Export All Distros
- Backup all distros at once, or select specific ones
- Perfect for system-wide backups before updates
- Add notes that apply to all backups

### 3. Clone a Distro
- Instant distro cloning without manual steps
- Select source distro → provide new name → done!
- Great for testing and experimentation

### 4. Import a Distro
- Restore from saved backups
- Choose custom name and install location
- Automatic decompression and cleanup

### 5. Manage Backups
Interactive backup management with sub-menu:
- **List all backups** - view all backups with size and date info
- **View backup details** - see full metadata including notes
- **Delete backups** - safely remove old backups with confirmation
- **Rename backups** - organize your backup library

### 6. Set Backup Directory
- Change default backup location
- Supports Windows and Unix-style paths
- Automatic quote stripping and path normalization

---

## 📁 File Structure

### Backup Storage
Default: `~/wsl_backups/` _(customizable)_

Each backup consists of:
- `Ubuntu-2026-03-15.tar.gz` - Compressed distro snapshot
- `Ubuntu-2026-03-15.tar.gz.meta.json` - Metadata file

### Metadata Example
```json
{
    "original_distro": "Ubuntu",
    "created_date": "2026-03-15 14:30:00",
    "wsl_version": 2,
    "size_compressed_mb": 1843.21,
    "notes": "Before kernel upgrade",
    "created_by": "wsl_snapshot_manager"
}
```

### Imported Distros
Default install location: `~/wsl_installs/<distro_name>/` _(customizable)_

---

## 🎯 Common Workflows

### Quick Experimentation
```
1. Clone a distro (option 3)
2. Test changes in the clone
3. Delete clone when done
```

### System Backup Before Updates
```
1. Export all distros (option 2)
2. Add note: "Before Windows Update"
3. Perform system updates
4. Keep backups for rollback if needed
```

### Manage Old Backups
```
1. Go to Manage backups (option 5)
2. List all backups to see sizes
3. Delete old/unnecessary backups
4. Rename important ones for clarity
```

---

## 🧹 Path Handling

The tool properly handles all these path formats:

```bash
# Windows-style
C:\Users\YourName\wsl_backups
"C:\Users\YourName\wsl_backups"

# Unix-style (Git Bash)
/c/Users/YourName/wsl_backups
"/c/Users/YourName/wsl_backups"

# Relative paths
./backups
../wsl_backups

# Home directory
~/wsl_backups
```

All paths are automatically normalized and directories are created as needed.

---

## 💡 Tips

- **Add descriptive notes** when creating backups - you'll thank yourself later!
- **Use Clone instead of export+import** when you need a quick copy
- **Export all before major changes** - system updates, WSL upgrades, etc.
- **Review backups regularly** using the Manage Backups menu
- **Metadata is your friend** - it helps you remember why you created each backup

---

## 🚀 Future Features

See [FEATURE_IDEAS.md](FEATURE_IDEAS.md) for planned improvements including:
- Auto-cleanup with retention policies
- Differential exports
- Backup integrity verification
- Compression level options
- And more!

---

## 🛡️ License

This project is licensed under the **MIT License**.  
Feel free to use, modify, and contribute!

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs via GitHub issues
- Suggest new features
- Submit pull requests
- Share your use cases

---

## 📝 Changelog

### v2.0 (Latest)
- ✨ Added backup metadata with notes
- ✨ Added clone distro feature
- ✨ Added export all distros
- ✨ Added backup management (list, view, delete, rename)
- 🐛 Fixed path handling issues
- 🐛 Fixed quote stripping in paths

### v1.0
- Initial release
- Basic export/import functionality
