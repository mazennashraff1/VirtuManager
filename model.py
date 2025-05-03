import os
import subprocess


def create_virtual_disk(disk_name, disk_path, disk_format, disk_size):
    full_path = os.path.join(disk_path, f"{disk_name}.{disk_format}")
    cmd = [
        r"C:/msys64/ucrt64/bin/qemu-img.exe",
        "create",
        "-f",
        disk_format,
        full_path,
        disk_size,
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"Disk {full_path} created successfully.")
    except subprocess.CalledProcessError as e:
        print("Error creating disk:", e)


def create_virtual_machine(disk_path, memory, cpu, iso):
    cmd = [
        r"C:/msys64/ucrt64/bin/qemu-img.exe",
        "-hda",
        disk_path,
        "-nographic",
        "-m",
        memory,
        "-smp",
        cpu,
    ]
    if iso:
        cmd += ["-cdrom", iso, "-boot", "d"]

    try:
        subprocess.run(cmd)
    except subprocess.CalledProcessError as e:
        print("Error launching VM:", e)
