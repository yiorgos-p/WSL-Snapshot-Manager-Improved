# Feature Ideas for Future Development

These are potential improvements that could be added to WSL Snapshot Manager.

---

## Auto-Cleanup / Retention Policy
**Keep backups organized automatically**
- Configure retention rules: keep last N backups per distro, delete backups older than X days
- "Keep monthly snapshots" option to preserve one backup per month
- Preview cleanup actions before confirming deletion
- Prevents backup directory from growing infinitely

## Differential Export Option
**Save time and disk space**
- Skip export if distro hasn't changed since last backup
- Compare current state with last backup before exporting
- Option to force export even if unchanged
- Useful for frequent backup schedules

## Backup to Alternative Location
**One-time export without changing default directory**
- Export directly to USB drive or network location
- Useful for offsite/portable backups
- Doesn't modify your default backup directory setting
- Quick "backup to..." option in export menu

## Verify Backup Integrity
**Ensure backups are valid before you need them**
- Quick verification that .tar.gz file is not corrupted
- Test decompression without full import
- Show estimated restore time and space requirements
- Prevent wasting time on corrupt backups

## Set Default Distro for Quick Backup
**One-click backup for your main distro**
- Configure a favorite distro for instant backup
- "Quick backup" option in main menu
- Useful for users who primarily backup one distro
- Save keystrokes and time

## Compression Level Options
**Trade speed vs size based on your needs**
- Fast compression (less CPU time, larger files)
- Maximum compression (more CPU time, smaller files)  
- No compression (fastest, for SSDs/NVMe drives)
- Let users choose based on available CPU/disk resources

## Show Disk Space Info
**Prevent "out of space" surprises**
- Display available space in backup directory before operations
- Estimate space needed for export based on distro size
- Warning when running low on disk space
- Helps plan storage needs

## Import Preview
**Know what you're importing before extraction**
- Show distro name and WSL version from backup
- Preview metadata without extracting full backup
- Avoid importing the wrong backup by mistake
- Quick sanity check before committing to restore
