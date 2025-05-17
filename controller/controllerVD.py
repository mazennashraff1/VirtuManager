import os
import shutil
from model.vd import create_virtual_disk


class VirtualDiskController:
    def __init__(self):
        pass

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
            return False, "Invalid Space cores requested (zero value)."
        else:
            return False, "Invalid Space requested (negative value)."

    def _checkValidPath(self, filePath="", folderPath="", extension=[], create=False):
        """Check if the specified file or folder exists at the given path and optionally create the file."""
        if folderPath != "":
            if create:
                if os.path.isfile(filePath):
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

        if os.path.isfile(filePath):
            if extension:
                fileExt = os.path.splitext(filePath)[1][1:].lower()
                if fileExt in [ext.lower() for ext in extension]:
                    return "", True
            return (
                f"Invalid file extension. Expected one of: {', '.join(extension)}.",
                False,
            )

        if folderPath != "":
            if os.path.isdir(folderPath):
                return "", True
            return "The specified folder does not exist.", False

        return "No file or folder path provided.", False

    def _saveVD(self, diskName, diskPath, diskFormat, diskSize):
        fileName = "./logs/allVD.txt"
        os.makedirs(os.path.dirname(fileName), exist_ok=True)
        fileExists = os.path.isfile(fileName)

        with open(fileName, "a") as f:
            if not fileExists:
                f.write("Disk Path,Format,Size (GB)\n")
            fullDiskPath = os.path.join(diskPath, diskName).replace("\\", "/")
            f.write(f"{fullDiskPath},{diskFormat},{diskSize}\n")

    def readVDs(self):
        VDs = []
        fileName = "logs/allVD.txt"
        if os.path.isfile(fileName):
            with open(fileName, "r") as f:
                lines = f.readlines()
                if len(lines) > 1:
                    for line in lines[1:]:
                        diskPath, diskFormat, diskSize = line.strip().split(",")
                        VDs.append(
                            {
                                "Disk Path": diskPath,
                                "Format": diskFormat,
                                "Size (GB)": diskSize,
                            }
                        )
        return VDs

    def updateVD(self, oldDiskName, newDiskName, diskPath, diskFormat, diskSize):
        formats = ["qcow2", "vmdk", "vdi", "raw", "vhd"]
        if newDiskName != "" and diskFormat != "" and diskSize != "" and diskPath != "":
            if diskFormat not in formats:
                return f"Virtual disk Format selected '{diskFormat}'. Expected one of: {', '.join(formats)}."

            # Step 1: Delete the old disk file
            old_file_path = os.path.join(diskPath, oldDiskName)
            if not os.path.splitext(old_file_path)[1]:
                # If old file has no extension, assume any format
                for ext in formats:
                    possible_path = f"{old_file_path}.{ext}"
                    if os.path.exists(possible_path):
                        os.remove(possible_path)
                        break
            elif os.path.exists(old_file_path):
                os.remove(old_file_path)

            # Step 2: Remove the old entry from logs
            log_file = "logs/allVD.txt"
            if os.path.exists(log_file):
                with open(log_file, "r") as f:
                    lines = f.readlines()

                with open(log_file, "w") as f:
                    f.write(lines[0])  # keep header
                    for line in lines[1:]:
                        if oldDiskName not in line:
                            f.write(line)

            # Step 3: Create new disk using callVD
            result = self.callVD(newDiskName, diskPath, diskFormat, diskSize)
            return f"Disk updated. {result}"
        else:
            return "Please Fill out all the information"

    def callVD(self, diskName, diskPath, diskFormat, diskSize):
        formats = ["qcow2", "vmdk", "vdi", "raw", "vhd"]
        if diskName != "" and diskFormat != "" and diskSize != "" and diskPath != "":
            if diskFormat not in formats:
                return f"Virtual disk Format selected '{diskFormat}'. Expected one of: {', '.join(formats)}."

            pathMessage, dPath = self._checkValidPath(
                f"{diskPath}/{diskName}.{diskFormat}", diskPath, [diskFormat], True
            )
            if dPath:
                dSize, dMessage = self._validateDiskSpace(diskSize, diskPath)
                if dSize:
                    create_virtual_disk(diskName, diskPath, diskFormat, diskSize)
                    self._saveVD(diskName, diskPath, diskFormat, diskSize)
                    return (
                        f"Virtual disk '{diskName}' created successfully at {diskPath}."
                    )
                else:
                    return dMessage
            else:
                return pathMessage
        else:
            return "Please Fill out all the information"
