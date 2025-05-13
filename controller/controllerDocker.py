import os


class DockerController:
    def __init__():
        pass

    def parseDockerList(self, output: str):
        lines = output.strip().split("\n")
        headers = lines[0].split()
        containers = []

        for line in lines[1:]:
            values = line.split()
            container_info = {headers[i]: values[i] for i in range(len(headers))}
            containers.append(container_info)

        return containers
