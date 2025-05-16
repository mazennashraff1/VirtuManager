import subprocess
import os


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


def create_dockerfile_interactive(dockerfile_content,path, base_image, app_file):

    # dockerfile_content = f"""
    # FROM {base_image}
    # COPY . /app
    # WORKDIR /app
    # RUN pip install --no-cache-dir -r requirements.txt
    # CMD ["python", "{app_file}"]
    # """.strip()

    os.makedirs(path, exist_ok=True)
    dockerfile_path = os.path.join(path, "Dockerfile")
    with open(dockerfile_path, "w") as f:
        f.write(dockerfile_content)

    print(f"Dockerfile created at {dockerfile_path}")


def build_docker_image_interactive(path, tag):

    cmd = ["docker", "build", "-t", tag, path]
    try:
        subprocess.run(cmd, check=True)
        print(f"Docker image '{tag}' built successfully.")
    except subprocess.CalledProcessError as e:
        print("Error building Docker image:", e)


def search_local_images(query):
    """
    Searches for Docker images available locally that match a user-provided name or tag.
    """
    cmd = ["docker", "images", "--format", "{{.Repository}}:{{.Tag}} {{.ID}} {{.CreatedSince}} {{.Size}}"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split("\n")
        matches = [line for line in lines if query.lower() in line.lower()]
        if matches:
            print("Matching local Docker images:")
            for match in matches:
                print(" -", match)
        else:
            print("No local images found matching:", query)
    except subprocess.CalledProcessError as e:
        print("Error retrieving local Docker images:", e.stderr or str(e))

def search_dockerhub_images(query):
    """
    Searches DockerHub for public Docker images matching a user-provided query.
    """
    cmd = ["docker", "search", query]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("📦 DockerHub Search Results:\n")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error using 'docker search':", e.stderr or str(e))


if __name__ == "__main__":
    # create_dockerfile("myapp", base_image="python:3.9", app_file="app.py")

    # build_docker_image("myapp", tag="my-python-app")

    #pull_image("ubuntu")
    search_dockerhub_images("nginx")
