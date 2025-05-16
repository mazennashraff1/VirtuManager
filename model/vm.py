import os
import shutil
import subprocess
import signal
import time

vm_process = None  # Global reference to the running VM process


def get_qemu_system_path():
    qemu_system_path = shutil.which("qemu-system-x86_64")

    if qemu_system_path and os.path.isfile(qemu_system_path):
        return qemu_system_path

    fallback_paths = [
        r"C:\\msys64\\ucrt64\\bin\\qemu-system-x86_64.exe",
        r"C:\\msys64\\mingw64\\bin\\qemu-system-x86_64.exe",
        r"C:\\msys64\\clang64\\bin\\qemu-system-x86_64.exe",
    ]

    for path in fallback_paths:
        if os.path.isfile(path):
            return path

    raise FileNotFoundError("qemu-system-x86_64.exe not found.")


def is_process_running(pid):
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def create_virtual_machine(disk_path, memory, cpu_cores, iso):
    global vm_process
    qemu_system_path = get_qemu_system_path()

    cmd = [
        qemu_system_path,
        "-m",
        str(memory),  # Set RAM
        "-cpu",
        "max",  # Use all CPU features
        "-smp",
        str(cpu_cores),  # Set number of cores
        "-hda",
        disk_path,  # Disk image
        "-cdrom",
        iso,  # ISO file
        "-boot",
        "menu=on",  # Boot menu
        "-display",
        "sdl",  # GUI window
    ]

    print("Running command:", " ".join(cmd))

    try:
        vm_process = subprocess.Popen(cmd)
        with open("vm.pid", "w") as f:
            f.write(str(vm_process.pid))
        print(f"VM started with PID {vm_process.pid}")
        return vm_process.pid
    except Exception as e:
        print("Error launching VM:", e)


def stop_virtual_machine(pid):
    try:
        print(f"Stopping VM with PID {pid}...")
        os.kill(int(pid), signal.SIGTERM)
        print("VM stopped successfully.")
    except ProcessLookupError:
        print("No such process. VM may have already exited.")
    except PermissionError:
        print("Permission denied. Try running with elevated privileges.")
    except Exception as e:
        print(f"Error stopping VM: {e}")


if __name__ == "__main__":
    create_virtual_machine(
        "C:/Users/ahmed/OneDrive/Desktop/Learn/MSA/cloud/VirtuManager/test.qcow2",
        1024,
        2,
        "C:/Users/ahmed/OneDrive/Desktop/Learn/MSA/cloud/linuxmint-22-cinnamon-64bit.iso",
    )

    time.sleep(10)
    stop_virtual_machine()
