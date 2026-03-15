# WSL Snapshot Manager - Basic Version

This is the **basic version** with original functionality and critical bug fixes.

**Looking for the expanded version?** → [README_EXPANDED.md](./README_EXPANDED.md)

---

## ✨ What's Fixed

This version fixes the critical path handling bugs from the original tool:

✅ **Path handling with quotes** - No more errors when paths contain quotes  
✅ **Mixed path separators** - Properly handles Windows and Unix-style paths  
✅ **Automatic directory creation** - Backup directories created automatically  
✅ **Path normalization** - All paths properly normalized before use  
✅ **Config reloading** - Menu shows updated paths immediately

---

## 🚀 Features

- 📦 **Export WSL distros** into compressed `.tar.gz` snapshots
- 🛠 **Import snapshots** back into WSL
- 📂 **Customizable backup directory**
- 🎨 **Colored output** for better UX
- 🔄 **Progress spinner** during operations
- ⚡ **Auto-detects** WSL1 or WSL2 versions

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/wsl-snapshot-manager.git
cd wsl-snapshot-manager

# Install dependencies
pip install -r requirements.txt

# Run the tool
python wsl_snapshot_manager_basic.py
```

---

## 📋 Usage

You will see an interactive menu:

```
WSL Snapshot Manager
---
The default export(backup) directory is C:\Users\YourName\wsl_backups
---

1. Export a WSL distro
2. Import a WSL distro
3. Set backup directory
4. Exit
```

### Export a Distro
- Select an installed WSL distro
- Backup is created and compressed automatically
- Saved to your backup directory

### Import a Distro
- Select a saved backup
- Provide a name for the new distro
- Choose install location (or use default)

### Set Backup Directory
- Change where backups are saved
- Supports all path formats (see below)
- Directory created automatically

---

## 🧹 Path Handling

The tool correctly handles all these path formats:

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

All paths are automatically:
- **Quote-stripped** - Removes surrounding quotes
- **Normalized** - Consistent separators
- **Expanded** - `~` converted to home directory
- **Created** - Directories made if they don't exist

---

## 📁 Default Locations

- **Backup storage**: `~/wsl_backups/` _(customizable)_
- **Imported distros**: `~/wsl_installs/<distro_name>/` _(customizable)_

---

## 🛠 Requirements

- **Python 3.7+**
- **Windows 10/11** with WSL installed
- **termcolor** package (installed via requirements.txt)

---

## 🔧 What's NOT Included

This is the **basic version** - it does not include:
- Export all distros at once
- Clone distro feature
- Backup management (list/delete/rename)
- Backup metadata and notes

**Want these features?** Use the [Expanded Version](./README_EXPANDED.md)

---

## 📝 What Changed From Original

See [BUG_ANALYSIS_AND_FIXES.md](./BUG_ANALYSIS_AND_FIXES.md) for detailed technical explanation of all fixes.

**Summary:**
- Fixed path handling bugs that caused export failures
- Added automatic directory creation
- Added path normalization
- Added quote stripping
- Fixed config reloading

---

## 🛡️ License

MIT License - See [LICENSE](./LICENSE) file for details.

---

## 🔗 Related

- [Main README](./README.md) - Choose between Basic and Expanded versions
- [Expanded Version](./README_EXPANDED.md) - Full-featured version
- [Bug Fixes Documentation](./BUG_ANALYSIS_AND_FIXES.md)
