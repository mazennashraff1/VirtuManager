import os
import psutil
import shutil
from model import create_virtual_disk, create_virtual_machine


class Controller:
    def __init__(self):
        self._freeRAM = psutil.virtual_memory()
        self._numberOfCores = psutil.cpu_count(logical=True)

    def _validateDiskSpace(self, requiredGB, targetPath=""):
        """Check if there is enough free disk space for the required virtual disk."""
        self._totalSpace, self._usedSpace, self._freeSpace = shutil.disk_usage(
            targetPath
        )
        freeGB = self._freeSpace / (1024**3)  # Convert bytes to GB

        if int(requiredGB) > freeGB:
            return (
                False,
                f"Not enough space: {freeGB:.2f} GB available, but {requiredGB} GB required.",
            )
        else:
            return True, f"Enough space: {freeGB:.2f} GB available."

    def _checkValidPath(self, filePath="", folderPath="", extension=[]):
        """Check if the specified file or folder exists at the given path."""
        if filePath != "":
            if os.path.isfile(filePath):
                if extension:
                    fileExt = os.path.splitext(filePath)[1][1:].lower()
                    if fileExt in [ext.lower() for ext in extension]:
                        return "", True
                return (
                    f"Invalid file extension. Expected one of: {', '.join(extension)}.",
                    False,
                )

        # Check if folderPath is provided
        if folderPath != "":
            if os.path.isdir(folderPath):
                return "", True
            return "The specified folder does not exist.", False

        return "No file or folder path provided.", False

    def _checkValidRAM(self, requiredRAM):
        """Check if the system has enough available RAM for the VM."""
        ram = self._freeRAM.total / (1024**3)  # Convert to GB
        if int(requiredRAM) <= ram:
            return True
        return False

    def _checkValidCPU(self, requiredCPU):
        """Check if the system has enough CPU cores for the VM."""
        if int(requiredCPU) <= self._numberOfCores:
            return True
        return False

    def callVM(self, diskPath, requiredRAM, requiredCPU, isoPath):
        """Create a virtual machine if all system requirements (disk, RAM, CPU, ISO file) are met."""
        response = ""
        ext, disk = self._checkValidPath(
            diskPath,
            "",
            [
                "qcow2",
                "vmdk",
                "vdi",
                "raw",
                "vhd",
                "vhdx",
                "vbox",
                "hdd",
                "img",
                "dmg",
                "qed",
                "vzdisk",
                "zfs",
            ],
        )
        ram = self._checkValidRAM(requiredRAM)
        cpu = self._checkValidCPU(requiredCPU)
        iso = self._checkValidPath(isoPath, "", ["iso", "img"])[
            1
        ]  # Validate ISO path, we only care about the boolean result
        if disk and ram and cpu and iso:
            create_virtual_machine(diskPath, requiredRAM, requiredCPU, isoPath)
            return "Creating VM Successfully"
        else:
            if not disk:
                response += ext + "\n"
            if not ram:
                response += f"Insufficient RAM. Available RAM: {self._freeRAM.total / (1024**3):.2f} GB, Required: {requiredRAM} GB.\n"
            if not cpu:
                response += f"Insufficient CPU cores. Available cores: {self._numberOfCores}, Required: {requiredCPU} cores.\n"
            if not iso:
                response += "The ISO path is invalid or the ISO file is not found. \n"
            return response

    def callVD(self, diskName, diskPath, diskFormat, diskSize):
        pathMessage, dPath = self._checkValidPath("", diskPath, [])
        if dPath:
            dSize, dMessage = self._validateDiskSpace(diskSize, diskPath)
            if dSize:
                create_virtual_disk(diskName, diskPath, diskFormat, diskSize)
                return f"Virtual disk '{diskName}' created successfully at {diskPath}."
            else:
                return dMessage
        else:
            return pathMessage
