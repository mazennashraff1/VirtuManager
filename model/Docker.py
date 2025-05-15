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
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Error listing all containers:", e)
        return ""


def pull_image(image_name: str):
    """
    Pulls a Docker image from DockerHub.

    Args:
        image_name (str): The name of the image (e.g. 'nginx', 'python:3.11-alpine')
    """
    print(f"Pulling image '{image_name}' from DockerHub...")
    cmd = ["docker", "pull", image_name]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Image pulled successfully.\n")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error pulling image:")
        print(e.stderr if e.stderr else str(e))


def create_dockerfile(content, path):
    try:
        with open(path, "w") as f:
            f.write(content)
            print(f"Dockerfile created at {path}")
            return True, f"Dockerfile created at {path}"
    except Exception as e:
        return False, f"Failed to save Dockerfile: {str(e)}"


def build_docker_image(docker_path, create_path, tag):
    cmd = ["docker", "build", "-f", docker_path, "-t", tag, create_path]

    try:
        subprocess.run(cmd, check=True)
        return True, f"Docker image '{tag}' built successfully."
    except subprocess.CalledProcessError as e:
        return False, f"Error building Docker image: {e}"


def list_all_images():
    return
