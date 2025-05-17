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
        return (
            False,
            "Unable to list containers. Make sure Docker is running and you have the necessary permissions.",
        )


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
    except subprocess.CalledProcessError:
        return (
            False,
            "Unable to list images. Ensure Docker is running and accessible from your terminal.",
        )


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
        return (
            False,
            f"Failed to run container.\nDetails: {e.stderr.strip() if e.stderr else str(e)}\nTip: Check if the image exists locally or if the ports are already in use.",
        )


def stop_container(container_id):
    cmd = ["docker", "stop", container_id]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return (
            True,
            f"Container '{container_id}' stopped successfully.\n{result.stdout.strip()}",
        )
    except subprocess.CalledProcessError as e:
        return (
            False,
            f"Failed to stop container '{container_id}'.\nDetails: {e.stderr.strip()}\nMake sure the container is running.",
        )


def start_container(container_id_or_name):
    cmd = ["docker", "start", container_id_or_name]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return (
            True,
            f"Container '{container_id_or_name}' started successfully.\n{result.stdout.strip()}",
        )
    except subprocess.CalledProcessError as e:
        return (
            False,
            f"Failed to start container '{container_id_or_name}'.\nDetails: {e.stderr.strip()}\nCheck if the container exists or is already running.",
        )


def delete_image(image_name_or_id):
    cmd = ["docker", "rmi", image_name_or_id]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return (
            True,
            f"Image '{image_name_or_id}' deleted successfully.\n{result.stdout.strip()}",
        )
    except subprocess.CalledProcessError as e:
        return (
            False,
            f"Could not delete image '{image_name_or_id}'.\nDetails: {e.stderr.strip()}\nTip: Ensure the image is not used by any containers.",
        )


def delete_container(container_name_or_id):
    cmd = ["docker", "rm", container_name_or_id]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return (
            True,
            f"Container '{container_name_or_id}' deleted successfully.\n{result.stdout.strip()}",
        )
    except subprocess.CalledProcessError as e:
        return (
            False,
            f"Could not delete container '{container_name_or_id}'.\nDetails: {e.stderr.strip()}\nTip: Stop the container before deleting it.",
        )


def pull_image(image_name: str):
    cmd = ["docker", "pull", image_name]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, f"Image '{image_name}' pulled successfully."
    except subprocess.CalledProcessError as e:
        return (
            False,
            f"Failed to pull image '{image_name}'.\nDetails: {e.stderr.strip() if e.stderr else str(e)}\nEnsure the image name is correct and you have internet access.",
        )


def create_dockerfile(content, path):
    try:
        with open(path, "w") as f:
            f.write(content)
        return True, f"Dockerfile saved successfully at: {path}"
    except Exception as e:
        return (
            False,
            f"Error saving Dockerfile: {str(e)}\nCheck if the path is correct and you have write permissions.",
        )


def build_docker_image(docker_path, create_path, tag):
    cmd = ["docker", "build", "-f", docker_path, "-t", tag, create_path]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, f"Docker image '{tag}' built successfully."
    except subprocess.CalledProcessError as e:
        return (
            False,
            f"Failed to build image '{tag}'.\nDetails: {e.stderr.strip() if e.stderr else str(e)}\nEnsure the Dockerfile is valid and the build context path is correct.",
        )


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
            return (
                False,
                "No image found matching your query.\nTry pulling it first using the image name.",
            )
    except subprocess.CalledProcessError as e:
        return (
            False,
            f"Could not search local images.\nDetails: {e.stderr.strip() if e.stderr else str(e)}\nIs Docker running?",
        )
