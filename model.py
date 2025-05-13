import os
import subprocess
import shutil
import os


def get_qemu_img_path():
    qemu_img_path = shutil.which("qemu-img")

    if qemu_img_path and os.path.isfile(qemu_img_path):
        return qemu_img_path

    fallback_paths = [
        r"C:\\msys64\\ucrt64\\bin\\qemu-img.exe",
        r"C:\\msys64\\mingw64\\bin\\qemu-img.exe",
        r"C:\\msys64\\clang64\\bin\\qemu-img.exe",
        r"C:\\msys64\\msys\\bin\\qemu-img.exe",
        r"C:\\msys64\\mingw32\\bin\\qemu-img.exe",
        r"C:\\msys64\\clang32\\bin\\qemu-img.exe",
        r"C:\\msys64\\clangarm64\\bin\\qemu-img.exe",
    ]

    for path in fallback_paths:
        if os.path.isfile(path):
            return path

    raise FileNotFoundError(
        "qemu-img.exe was not found in system PATH or any known MSYS2 environments."
    )


def create_virtual_disk(disk_name, disk_path, disk_format, disk_size):
    full_path = os.path.join(disk_path, f"{disk_name}.{disk_format}")
    qemu_img_path = get_qemu_img_path()
    if disk_format != "vhd":
        cmd = [
            qemu_img_path,
            "create",
            "-f",
            disk_format,
            full_path,
            disk_size + "G",
        ]
    else:
        cmd = [
            qemu_img_path,
            "create",
            "-f",
            "vpc",
            full_path,
            disk_size + "G",
        ]
    try:
        subprocess.run(cmd, check=True)
        print(f"Disk {full_path} created successfully.")
    except subprocess.CalledProcessError as e:
        print("Error creating disk:", e)


def create_virtual_machine(disk_path, memory, cpu, iso):
    qemu_img_path = get_qemu_img_path()
    cmd = [
        qemu_img_path,
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


def list_running_containers():
    cmd = ["docker", "ps"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error listing running containers:", e)
