import os
import requests
from model.Docker import pull_image


class DockerController:
    def __init__(self):
        pass

    def parseDockerList(self, output: str):
        lines = output.strip().split("\n")
        headers = lines[0].split()
        containers = []

        for line in lines[1:]:
            values = line.split()
            containerInfo = {headers[i]: values[i] for i in range(len(headers))}
            containers.append(containerInfo)

        return containers

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
