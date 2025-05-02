# VirtuManager

**VirtuManager** is a Python-based graphical application designed to help users easily create and manage virtual disks and virtual machines. The tool provides system validation checks for CPU, RAM, and disk space before making a virtual machine, ensuring optimal configuration.

This project is the first phase of a broader virtualization and container management tool.

## 🚀 Features (Phase 1)
✅ Create virtual disks by specifying name, path, format, and size  
✅ Create virtual machines by specifying CPU, RAM, disk, and ISO image  
✅ Validates available system resources (CPU cores, RAM, disk space) before creating a VM  
✅ Supports multiple virtual disk formats: `qcow2`, `vmdk`, `vdi`, `raw`, `vhd`, `vhdx`, `vbox`, `hdd`, `img`, `dmg`, `qed`, `vzdisk`, `zfs`

## 🖥️ Technologies Used
- **Python 3.x**
- **tkinter** for GUI
- **psutil** for system resource monitoring
- **shutil** and **os** for file system operations

## 📂 Project Structure
VirtuManager/
- `controller.py`       # Main logic for system checks and operations
- `model.py`            # Contains methods to create VM and virtual disks
- `view.py`             # GUI implementation with tkinter

## ⚙️ How to Run
1. Install dependencies:
   ```bash
   pip install psutil
   
## 📌 Notes
- This project currently supports creating virtual disks and virtual machines only.
- More features, such as Docker management, will be added in future phases.

## 💡 Future Enhancements
Planned features for upcoming phases:

- Dockerfile creation
- Docker image building
- Docker container management (list, stop, search, pull)
