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
        "order=d,menu=on",  # Boot menu
        "-display",
        "sdl",  # GUI window
    ]

    print("Running command:", " ".join(cmd))

    try:
        vm_process = subprocess.Popen(cmd)
        with open("vms.pid", "a") as f:
            f.write(f"{disk_path},{vm_process.pid}\n")
        print(f"VM started with PID {vm_process.pid}")
        return vm_process.pid
    except Exception as e:
        print("Error launching VM:", e)


def stop_virtual_machine(pid):
    try:
        result = subprocess.run(
            ["taskkill", "/PID", str(pid), "/F"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ VM process {pid} terminated.")
    except subprocess.CalledProcessError as e:
        if "not found" in e.stderr.lower() or "no running instance" in e.stderr.lower():
            print(f"⚠️ VM process {pid} is already stopped or not found.")
        else:
            print(f"❌ Failed to stop VM {pid}:\n{e.stderr.strip()}")


def stop_vm_by_disk_path(disk_path):
    pid_to_kill = None

    try:
        with open("vms.pid", "r") as f:
            lines = f.readlines()
        for line in lines:
            path, pid = line.strip().split(",")
            if path == disk_path:
                pid_to_kill = pid
                break
    except FileNotFoundError:
        print("❌ vms.pid file not found.")
        return

    if not pid_to_kill:
        print(f"⚠️ No running VM found for disk path: {disk_path}")
        return

    stop_virtual_machine(pid_to_kill)
    remove_vm_pid_entry(disk_path)


def remove_vm_pid_entry(disk_path):
    try:
        with open("vms.pid", "r") as f:
            lines = f.readlines()
        with open("vms.pid", "w") as f:
            for line in lines:
                if not line.startswith(disk_path):
                    f.write(line)
        print(f"🧹 Cleaned up PID entry for: {disk_path}")
    except Exception as e:
        print(f"❌ Failed to update vms.pid: {e}")


if __name__ == "__main__":
    create_virtual_machine(
        "C:/Users/ahmed/OneDrive/Desktop/Learn/MSA/cloud/VirtuManager/test.qcow2",
        1024,
        2,
        "C:/Users/ahmed/OneDrive/Desktop/Learn/MSA/cloud/linuxmint-22-cinnamon-64bit.iso",
    )

    time.sleep(10)
    stop_virtual_machine()
