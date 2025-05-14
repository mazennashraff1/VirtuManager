import subprocess


def list_running_containers():
    cmd = ["docker", "ps"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error listing running containers:", e)


def list_all_containers():
    cmd = ["docker", "ps", "-a"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error listing all containers:", e)


def pull_image(image_name):
    return
