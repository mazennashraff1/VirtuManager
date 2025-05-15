import os
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
        if output != "":
            lines = output.strip().split("\n")
            containers = []

            for line in lines:
                parts = line.split()
                print(parts)
                statusStr = parts[2]
                isRunning = statusStr.startswith("Up")
                container = {
                    "ID": parts[0],
                    "Name": parts[1],
                    "Status": parts[2],
                    "Image": parts[-1],
                    "Running": isRunning,
                }
                containers.append(container)

            return containers
        return ""

    def _parseDockerImages(self, output: str):
        lines = output.strip().split("\n")
        images = []

        if len(lines) <= 1:
            return images

        # Skip header
        for line in lines[1:]:
            parts = line.split(maxsplit=4)
            if len(parts) < 5:
                continue

            image = {
                "Repository": parts[0],
                "Tag": parts[1],
                "ImageID": parts[2],
                "Created": parts[3],
                "Size": parts[4],
            }
            images.append(image)

        return images

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

    def saveEditedDockerFile(self, id, path, content, description):
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
        self._saveLog(data)

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

        dockerFileCheck = self._checkPath(dockerFile)
        if not dockerFileCheck:
            return False, "Please Provide a Valid Path of the DockerFile"

        buildDirCheck = self._checkPath(buildDir)
        if not buildDirCheck:
            return False, "Please Provide a Valid Path to save the Build in it"

        imageTag = f"{name}:{tag}"
        return build_docker_image(dockerFile, buildDir, imageTag)

    def getAllContainers(self):
        output = list_all_containers()
        print(output)
        containers = self._parseDockerList(output)
        return containers

    def getAllImages(self):
        output = list_all_images()
        images = self._parseDockerImages(output)
        return images

    def fetchDockerImages(self, query, pageSize=5):
        try:
            url = f"https://hub.docker.com/v2/search/repositories/?query={query}&page_size={pageSize}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("results", [])
        except Exception as e:
            raise RuntimeError(f"Failed to fetch images: {str(e)}")

    def pullDockerImage(self, image: str) -> str:
        pull_image(image)

    def runDockerImage(self, imgName, imgTag, contName, hostPort, contPort):
        imgName = f"{imgName}:{imgTag}"
        return run_image(imgName, contName, hostPort, contPort)

    def startContainer(self, id):
        return start_container(id)

    def stopContainer(id):
        return stop_container(id)

    def deleteImage(id):
        return delete_image(id)
