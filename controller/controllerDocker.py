import re
import os
import socket
import requests
from model.Docker import (
    run_image,
    pull_image,
    delete_image,
    stop_container,
    list_all_images,
    start_container,
    create_dockerfile,
    build_docker_image,
    list_all_containers,
    search_local_images,
    delete_container,
)


class DockerController:
    def __init__(self):
        pass

    def _checkPath(self, path: str) -> bool:
        if os.path.isfile(path):
            return True
        elif os.path.isdir(path):
            return True
        else:
            return False

    def _parseDockerList(self, output: str):
        lines = output.strip().split("\n")
        containers = []

        if len(lines) <= 0:
            return containers

        for line in lines:
            parts = line.split()

            name = parts[0]
            container_id = parts[1]
            status = " ".join(parts[2:-1])
            image = parts[-1]
            is_running = status.startswith("Up")

            container = {
                "Name": name,
                "ID": container_id,
                "Status": status,
                "Image": image,
                "Running": is_running,
            }
            containers.append(container)

        return containers

    def _parseDockerImages(self, output: str):
        lines = output.strip().split("\n")
        images = []

        if len(lines) <= 0:
            return images

        # Skip header
        for line in lines:
            parts = line.split()
            nameID = parts[0]  # test:123
            image_id = parts[1]  # de072b06a269
            created = " ".join(parts[2:-1])  # About a minute ago
            size = parts[-1]
            name, tag = nameID.split(":")
            image = {
                "Repository": name,
                "Tag": tag,
                "ImageID": image_id,
                "Created": created,
                "Size": size,
            }
            images.append(image)

        return images

    def _validateHostPort(self, port: int) -> tuple[bool, str]:
        if not isinstance(port, int):
            return False, "Host port must be an integer."

        if port < 1 or port > 65535:
            return False, "Host port must be between 1 and 65535."

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", port)) == 0:
                return False, f"Host port {port} is already in use."

        return True, "Host port is valid and available."

    def _validateContPort(self, port: int) -> tuple[bool, str]:
        if not isinstance(port, int):
            return False, "Container port must be an integer."

        if port < 1 or port > 65535:
            return False, "Container port must be between 1 and 65535."

        # Optional: Add custom logic to check if this is a standard port based on image
        return True, "Container port is valid."

    def _saveLog(self, data):
        fileName = "logs/allDockerFiles.txt"
        os.makedirs(os.path.dirname(fileName), exist_ok=True)
        fileExists = os.path.isfile(fileName)

        lastID = 0
        if fileExists:
            with open(fileName, "r") as f:
                lines = f.readlines()
                if len(lines) > 1:
                    last_line = lines[-1].strip()
                    if last_line:
                        try:
                            lastID = int(last_line.split(",")[0])
                        except ValueError:
                            lastID = 0

        newID = lastID + 1

        with open(fileName, "a") as f:
            if not fileExists:
                f.write("ID,File Path,Description\n")
            f.write(f"{newID},{data['Path']},{data['desc']}\n")

    def _editLog(self, id, data):
        fileName = "logs/allDockerFiles.txt"
        os.makedirs(os.path.dirname(fileName), exist_ok=True)

        with open(fileName, "r") as f:
            lines = f.readlines()

            header = lines[0] if lines else ""
            new_lines = [header]
            edited = False

            for line in lines[1:]:
                parts = line.strip().split(",", 2)
                if len(parts) >= 3 and parts[0] == str(id):
                    # Edit this line only
                    new_lines.append(f"{id},{data['Path']},{data['desc']}\n")
                    edited = True
                else:
                    new_lines.append(line)

            if edited:
                with open(fileName, "w") as f:
                    f.writelines(new_lines)

    def _readLog(self):
        fileName = "logs/allDockerFiles.txt"
        data = []

        if not os.path.isfile(fileName):
            return data

        with open(fileName, "r") as f:
            lines = f.readlines()

            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",", 2)
                if len(parts) == 3:
                    try:
                        entry = {
                            "ID": int(parts[0]),
                            "Path": parts[1],
                            "desc": parts[2],
                        }
                        data.append(entry)
                    except ValueError:
                        continue

        return data

    def getDockerFileContent(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()

    def EditedDockerFile(self, id, path, content, description):
        if not path or not content:
            return False, "Both path and content are required."

        pth = self._checkPath(path)
        if not pth:
            return False, "Please Provide a Valid Path to Create a DockerFile in it"

        response, msg = create_dockerfile(content, path)

        if not response:
            return False, msg

        path = path.replace("\\", "/")
        data = {"Path": path, "desc": description}
        self._editLog(id, data)

        return response, msg

    def readDockerfiles(self):
        return self._readLog()

    def saveDockerFile(self, path, content, description):
        if not path or not content:
            return False, "Both path and content are required."

        pth = self._checkPath(path)
        if not pth:
            return False, "Please Provide a Valid Path to Create a DockerFile in it"

        path = os.path.join(path, "Dockerfile")
        response, msg = create_dockerfile(content, path)

        if not response:
            return False, msg

        path = path.replace("\\", "/")
        data = {"Path": path, "desc": description}
        self._saveLog(data)

        return response, msg

    def buildDockerImage(self, name, tag, dockerFile, buildDir):
        if not all([name, tag, dockerFile, buildDir]):
            return False, "All fields are required."

        # Validate image name
        valid_name = re.fullmatch(r"[a-z0-9._-]+", name)
        if not valid_name or name[0] in ".-_" or name[-1] in ".-_":
            return (
                False,
                "Invalid image name. Use only lowercase letters, numbers, '.', '-', '_' and do not start or end with separators.",
            )

        # Validate tag (optional, but can be added for stricter enforcement)
        valid_tag = re.fullmatch(r"[a-zA-Z0-9_.-]+", tag)
        if not valid_tag:
            return False, "Invalid tag. Use only letters, numbers, '.', '-', or '_'"

        # Check if image already exists locally
        existing_images = self.getAllImages()
        for img in existing_images:
            if img["Repository"] == name and img["Tag"] == tag:
                return False, f"Image '{name}:{tag}' already exists."

        dockerFileCheck = self._checkPath(dockerFile)
        if not dockerFileCheck:
            return False, "Please Provide a Valid Path of the DockerFile"

        # Check if Dockerfile is a file and readable
        if not os.path.isfile(dockerFile):
            return False, "Dockerfile path is not a file."
        try:
            with open(dockerFile, "r") as f:
                content = f.read()
                if "FROM" not in content.upper():
                    return (
                        False,
                        "Invalid Dockerfile. It must contain a FROM instruction.",
                    )
        except Exception as e:
            return False, f"Cannot read Dockerfile: {str(e)}"

        buildDirCheck = self._checkPath(buildDir)
        if not buildDirCheck:
            return False, "Please Provide a Valid Path to save the Build in it"

        imageTag = f"{name}:{tag}"
        return build_docker_image(dockerFile, buildDir, imageTag)

    def getAllContainers(self):
        res, output = list_all_containers()
        containers = self._parseDockerList(output)
        return containers

    def getAllImages(self):
        res, output = list_all_images()
        if res:
            images = self._parseDockerImages(output)
            return images
        else:
            return []

    def fetchDockerImages(self, query, pageSize=5):
        try:
            url = f"https://hub.docker.com/v2/search/repositories/?query={query}&page_size={pageSize}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("results", [])
        except Exception as e:
            raise RuntimeError(f"Failed to fetch images: {str(e)}")

    def pullDockerImage(self, image: str) -> tuple[bool, str]:
        try:
            # Default tag if not specified
            if ":" in image:
                img_name, img_tag = image.split(":")
            else:
                img_name = image
                img_tag = "latest"

            # Check if image already exists locally
            res, images = self.searchImage(img_name)
            if res:
                for img in images:
                    if img["Repository"] == img_name and img["Tag"] == img_tag:
                        return False, f"Image '{image}' is already pulled."

            # Pull the image
            return pull_image(image)

        except Exception as e:
            return False, f"Error pulling image: {str(e)}"

    def runDockerImage(self, imgName, imgTag, contName, hostPort, contPort):
        fullImageName = f"{imgName}:{imgTag}"

        # Check if image exists locally
        existing_images = self.getAllImages()
        exist = False
        for img in existing_images:
            if img["Repository"] == imgName and img["Tag"] == imgTag:
                exist = True

        if not exist:
            return (
                False,
                f"Image '{fullImageName}' not found locally. Please pull or build the image first.",
            )

        validHost, msgHost = self._validateHostPort(int(hostPort))
        if not validHost:
            return False, msgHost

        validCont, msgCont = self._validateContPort(int(contPort))
        if not validCont:
            return False, msgCont

        imgName = f"{imgName}:{imgTag}"
        return run_image(imgName, contName, hostPort, contPort)

    def startContainer(self, id):
        return start_container(id)

    def stopContainer(self, id):
        return stop_container(id)

    def deleteImage(self, id):
        return delete_image(id)

    def searchImage(self, name):
        valid_name = re.fullmatch(r"[a-z0-9._-]+", name)
        if not valid_name or name[0] in ".-_" or name[-1] in ".-_":
            return (
                False,
                "Invalid image name. Use only lowercase letters, numbers, '.', '-', '_' and do not start or end with separators.",
            )
        res, data = search_local_images(name)
        if res:
            images = self._parseDockerImages(data[0])
            return res, images
        else:
            return res, data

    def deleteContainer(self, id):
        return delete_container(id)
