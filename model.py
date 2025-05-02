import subprocess


def create_virtual_disk(disk_name, disk_format, disk_size):
    cmd = [
        "qemu-img",
        "create",
        "-f",
        disk_format,
        f"{disk_name}.{disk_format}",
        disk_size,
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"Disk {disk_name} created successfully.")
    except subprocess.CalledProcessError as e:
        print("Error creating disk:", e)


def create_virtual_machine(disk_path, memory, cpu, iso):
    cmd = [
        "qemu-system-x86_64",
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
