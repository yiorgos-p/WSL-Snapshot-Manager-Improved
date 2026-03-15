# 🐧 WSL Snapshot Manager

> ⚠️ **Two Versions Available** - Choose the one that fits your needs!

This repository contains **two versions** of WSL Snapshot Manager:

| Version | Description | Best For |
|---------|-------------|----------|
| **[Basic (Fixed)](./README_BASIC.md)** | Original tool with critical bug fixes | Users who want the original functionality with path handling fixed |
| **[Expanded](./README_EXPANDED.md)** | Enhanced version with new features | Power users who want backup management, cloning, bulk export, and metadata |

---

## 🔧 Basic Version (Bug Fixes Only)

**File:** `wsl_snapshot_manager.py`

✅ **Fixed Issues:**
- Path handling with quotes and mixed separators
- Automatic directory creation
- Path normalization for Windows/Unix paths
- Config reloading in main menu

✨ **Features:**
- Export WSL distros to compressed `.tar.gz`
- Import distros from backups
- Customizable backup directory
- Simple, clean interface

**[→ View Basic Version Documentation](./README_BASIC.md)**

---

## 🚀 Expanded Version (New Features)

**File:** `wsl_snapshot_manager_expanded.py`

Everything from Basic version, **PLUS:**

✨ **New Features:**
- 📊 **Export all distros** at once (bulk backup)
- 🔄 **Clone distros** instantly (one-click duplication)
- 🗂️ **Backup management** (list, view, delete, rename)
- 📝 **Backup metadata** with notes and automatic info

**[→ View Expanded Version Documentation](./README_EXPANDED.md)**

---

## 📦 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/wsl-snapshot-manager.git
cd wsl-snapshot-manager

# Install dependencies
pip install -r requirements.txt

# Run the version you prefer:
python wsl_snapshot_manager.py      # Basic version
# OR
python wsl_snapshot_manager_expanded.py   # Expanded version
```

---

## 🎯 Which Version Should I Use?

### Choose **Basic** if you:
- ✅ Want the original tool with bugs fixed
- ✅ Prefer simplicity and minimal features
- ✅ Just need basic export/import functionality
- ✅ Want the fastest, lightest version

### Choose **Expanded** if you:
- ✅ Manage multiple WSL distros regularly
- ✅ Need to clone distros for testing
- ✅ Want to organize and manage backup library
- ✅ Like adding notes to remember what each backup is for
- ✅ Prefer bulk operations (export all at once)

---

## 📋 Feature Comparison

| Feature | Basic | Expanded |
|---------|-------|----------|
| Export single distro | ✅ | ✅ |
| Import distro | ✅ | ✅ |
| Path bug fixes | ✅ | ✅ |
| Export all distros | ❌ | ✅ |
| Clone distro | ❌ | ✅ |
| Backup management | ❌ | ✅ |
| Metadata & notes | ❌ | ✅ |
| List backups | ❌ | ✅ |
| Delete/rename backups | ❌ | ✅ |

---

## 🛠 Requirements

- **Python 3.7+**
- **Windows 10/11** with WSL installed
- Dependencies: `pip install -r requirements.txt`

---

## 🤝 Contributing

Contributions are welcome! Both versions are maintained:
- **Bug fixes** → Submit to both versions
- **New features** → Submit to expanded version
- **Documentation** → Update relevant README

---

## 🛡️ License

MIT License - See [LICENSE](./LICENSE) file for details.

Original work by Ekin Akkaya  
Bug fixes and expanded features by me

---

## 📝 Credits

- **Original Author:** [Ekin Akkaya](https://github.com/ekinakkaya)
- **Bug Fixes & Expanded Version:** [Yiorgos Pinis](https://github.com/yiorgos-p)
