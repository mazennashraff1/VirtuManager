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


def create_virtual_machine(disk_path, memory, cpu, iso):
    global vm_process
    qemu_system_path = get_qemu_system_path()
    cmd = [
        qemu_system_path,
        "-hda",
        disk_path,
        "-m",
        str(memory),
        "-smp",
        str(cpu),
        "-cdrom",
        iso,
        "-boot",
        "d",
        "-cpu",
        "qemu64",
        "-display",
        "default",
    ]

    print("Running command:", " ".join(cmd))

    try:
        vm_process = subprocess.Popen(cmd)
        print(f"VM started with PID {vm_process.pid}")
    except Exception as e:
        print("Error launching VM:", e)


def stop_virtual_machine():
    global vm_process
    if vm_process and vm_process.poll() is None:
        print(f"Stopping VM with PID {vm_process.pid}...")
        vm_process.terminate()
        try:
            vm_process.wait(timeout=10)
            print("VM stopped successfully.")
        except subprocess.TimeoutExpired:
            print("VM did not shut down gracefully. Forcing termination...")
            vm_process.kill()
    else:
        print("No running VM to stop.")


if __name__ == "__main__":
    create_virtual_machine(
        "C:/Users/ahmed/OneDrive/Desktop/Learn/MSA/cloud/VirtuManager/test.qcow2",
        1024,
        2,
        "C:/Users/ahmed/OneDrive/Desktop/Learn/MSA/cloud/VirtuManager/linuxmint-22-cinnamon-64bit.iso",
    )

    time.sleep(15)
    stop_virtual_machine()
