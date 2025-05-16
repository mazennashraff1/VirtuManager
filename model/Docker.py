import subprocess


def list_all_containers():
    cmd = [
        "docker",
        "ps",
        "-a",
        "--format",
        "{{.ID}} {{.Names}} {{.Status}} {{.Image}}",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return False, f"Error listing all containers: {error_msg}"


def list_all_images():
    cmd = [
        "docker",
        "images",
        "--format",
        "{{.Repository}}:{{.Tag}} {{.ID}} {{.CreatedSince}} {{.Size}}",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return False, f"Error listing all images: {error_msg}"


def run_image(image_name, container_name, host_port, container_port):
    cmd = [
        "docker",
        "run",
        "-d",
        "--name",
        container_name,
        "-p",
        f"{host_port}:{container_port}",
        image_name,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return (
            True,
            f"Container '{container_name}' started successfully.\nID: {result.stdout.strip()}",
        )
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        return False, f"Failed to run container:\n{error_msg}"


def stop_container(container_id):
    cmd = ["docker", "stop", container_id]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return (
            True,
            f"Container '{container_id}' stopped successfully.\n{result.stdout.strip()}",
        )
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        return False, f"Failed to stop container '{container_id}': {error_msg}"


def start_container(container_id_or_name):
    cmd = ["docker", "start", container_id_or_name]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return (
            True,
            f"Container '{container_id_or_name}' started successfully.\n{result.stdout.strip()}",
        )
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        return False, f"Failed to start container:\n{error_msg}"


def delete_image(image_name_or_id):
    cmd = ["docker", "rmi", image_name_or_id]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return (
            True,
            f"Image '{image_name_or_id}' deleted successfully.\n{result.stdout.strip()}",
        )
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        return False, f"Failed to delete image:\n{error_msg}"


def delete_container(container_name_or_id):
    cmd = [
        "docker",
        "rm",
        container_name_or_id,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return (
            True,
            f"Container '{container_name_or_id}' deleted successfully.\n{result.stdout.strip()}",
        )
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        return False, f"Failed to delete container:\n{error_msg}"


def pull_image(image_name: str):
    """
    Pulls a Docker image from DockerHub.

    Args:
        image_name (str): The name of the image (e.g. 'nginx', 'python:3.11-alpine')

    Returns:
        (bool, str): Tuple where bool indicates success, and str is a message.
    """
    cmd = ["docker", "pull", image_name]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, f"Image '{image_name}' pulled successfully."
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return False, f"Error pulling image: {error_msg}"


def create_dockerfile(content, path):
    try:
        with open(path, "w") as f:
            f.write(content)
        return True, f"Dockerfile created at {path}"
    except Exception as e:
        return False, f"Failed to save Dockerfile: {str(e)}"


def build_docker_image(docker_path, create_path, tag):
    cmd = ["docker", "build", "-f", docker_path, "-t", tag, create_path]
    try:
        subprocess.run(cmd, check=True)
        return True, f"Docker image '{tag}' built successfully."
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return False, f"Error building Docker image: {error_msg}"


def search_local_images(query):
    cmd = [
        "docker",
        "images",
        "--format",
        "{{.Repository}}:{{.Tag}} {{.ID}} {{.CreatedSince}} {{.Size}}",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split("\n")
        matches = [line for line in lines if query.lower() in line.lower()]
        if matches:
            return True, matches
        else:
            return True, []
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return False, f"Error retrieving local Docker images: {error_msg}"
