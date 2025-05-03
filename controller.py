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
        if int(requiredGB) > 0:
            if int(requiredGB) > freeGB:
                return (
                    False,
                    f"Not enough space: {freeGB:.2f} GB available, but {requiredGB} GB required.",
                )
            else:
                return True, f"Enough space: {freeGB:.2f} GB available."
        elif int(requiredGB) == 0:
            return (
                False,
                f"The Space Requrired should be Greater than Zero.",
            )
        else:
            return (
                False,
                f"We Can't have Negative Space required.",
            )

    def _checkValidPath(self, filePath="", folderPath="", extension=[], create=False):
        """Check if the specified file or folder exists at the given path and optionally create the file."""
        if folderPath != "":
            if create:
                print(os.path.isfile(filePath))
                if os.path.isfile(filePath):
                    # Check if a file with the same extension already exists
                    print(filePath)
                    fileExt = os.path.splitext(filePath)[1][1:].lower()
                    for ext in extension:
                        if fileExt == ext.lower() and os.path.isfile(filePath):
                            return (
                                f"You are attempting to create a file already exists.",
                                False,
                            )

                # Create the file (if you want to create an empty file)
                with open(filePath, "w") as f:
                    pass
                return "", True

            # Check if file exists and matches extension
            if os.path.isfile(filePath):
                if extension:
                    fileExt = os.path.splitext(filePath)[1][1:].lower()
                    if fileExt in [ext.lower() for ext in extension]:
                        return "", True
                return (
                    f"Invalid file extension. Expected one of: {', '.join(extension)}.",
                    False,
                )

        if filePath != "":
            # Check if file exists and matches extension
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
        requiredRAM = int(requiredRAM)

        if requiredRAM < 0:
            return f"Invalid RAM size requested (negative value). Available RAM: {ram:.2f} GB, Requested: {requiredRAM} GB."
        elif requiredRAM == 0:
            return f"Invalid RAM size requested (zero value). Available RAM: {ram:.2f} GB, Requested: {requiredRAM} GB."
        elif requiredRAM > ram:
            return f"Insufficient RAM. Available: {ram:.2f} GB, Required: {requiredRAM} GB."

        return True

    def _checkValidCPU(self, requiredCPU):
        """Check if the system has enough CPU cores for the VM."""
        requiredCPU = int(requiredCPU)

        if requiredCPU < 0:
            return f"Invalid CPU cores requested (negative value). Available cores: {self._numberOfCores}, Requested: {requiredCPU}."
        elif requiredCPU == 0:
            return f"Invalid CPU cores requested (zero value). Available cores: {self._numberOfCores}, Requested: {requiredCPU}."
        elif requiredCPU > self._numberOfCores:
            return f"Insufficient CPU cores. Available: {self._numberOfCores}, Required: {requiredCPU}."

        return True

    def callVM(self, diskPath, requiredRAM, requiredCPU, isoPath):
        """Create a virtual machine if all system requirements (disk, RAM, CPU, ISO file) are met."""
        response = ""
        if diskPath != "" and requiredRAM != "" and requiredCPU != "" and isoPath != "":
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
            # Validate RAM and CPU
            ram = self._checkValidRAM(requiredRAM)
            cpu = self._checkValidCPU(requiredCPU)
            # Validate ISO path (only care if valid or not)
            cext, iso = self._checkValidPath(isoPath, "", ["iso", "img"])
            # If all checks pass
            if disk and ram == True and cpu == True and iso:
                create_virtual_machine(diskPath, requiredRAM, requiredCPU, isoPath)
                return "Creating VM Successfully"
            # Otherwise accumulate error messages
            if not disk:
                response += "Disk Path: " + ext + "\n"
            if ram != True:
                response += "RAM:" + ram + "\n"  # ram contains the error message
            if cpu != True:
                response += "CPU:" + cpu + "\n"  # cpu contains the error message
            if not iso:
                response += "ISO Path:" + cext + "\n"
            return response.strip()
        else:
            return "Please Fill out all the information"

    def callVD(self, diskName, diskPath, diskFormat, diskSize):
        formats = [
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
        ]
        if diskName != "" and diskFormat != "" and diskSize != "" and diskPath != "":
            if diskFormat not in formats:
                return f"Virtual disk Format selected '{diskFormat}'. Expected one of: {', '.join(formats)}."
            print(f"{diskPath}/{diskName}.{diskFormat}")
            pathMessage, dPath = self._checkValidPath(
                f"{diskPath}/{diskName}.{diskFormat}", diskPath, [diskFormat], True
            )
            if dPath:
                dSize, dMessage = self._validateDiskSpace(diskSize, diskPath)
                if dSize:
                    create_virtual_disk(diskName, diskPath, diskFormat, diskSize)
                    return (
                        f"Virtual disk '{diskName}' created successfully at {diskPath}."
                    )
                else:
                    return dMessage
            else:
                return pathMessage
        else:
            return "Please Fill out all the information"
