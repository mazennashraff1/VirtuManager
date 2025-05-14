import os
import psutil
from model.vm import create_virtual_machine


class VirtualMachineController:
    def __init__(self):
        self._freeRAM = psutil.virtual_memory()
        self._numberOfCores = psutil.cpu_count(logical=True)

    def _checkValidRAM(self, requiredRAM):
        """Check if the system has enough available RAM for the VM."""
        ram = self._freeRAM.total / (1024**3)  # Convert to GB
        requiredRAM = int(requiredRAM)
        if requiredRAM < 0:
            return f"Invalid RAM size requested (negative value)."
        elif requiredRAM == 0:
            return f"Invalid RAM size requested (zero value)."
        elif requiredRAM > ram:
            return f"Insufficient RAM. Available: {ram:.2f} GB, Required: {requiredRAM} GB."
        return True

    def _checkValidCPU(self, requiredCPU):
        """Check if the system has enough CPU cores for the VM."""
        requiredCPU = int(requiredCPU)
        if requiredCPU < 0:
            return f"Invalid CPU cores requested (negative value)."
        elif requiredCPU == 0:
            return f"Invalid CPU cores requested (zero value)."
        elif requiredCPU > self._numberOfCores:
            return f"Insufficient CPU cores. Available: {self._numberOfCores}, Required: {requiredCPU}."
        return True

    def _checkValidPath(self, filePath="", extension=[], create=False):
        """Check if the specified file exists at the given path and optionally create the file."""
        if os.path.isfile(filePath):
            if extension:
                fileExt = os.path.splitext(filePath)[1][1:].lower()
                if fileExt in [ext.lower() for ext in extension]:
                    return "", True
            return (
                f"Invalid file extension. Expected one of: {', '.join(extension)}.",
                False,
            )
        return "No file or folder path provided.", False

    def _saveVM(self, diskPath, RAM, CPU, isoPath):
        fileName = "logs/allVM.txt"
        os.makedirs(os.path.dirname(fileName), exist_ok=True)
        fileExists = os.path.isfile(fileName)

        with open(fileName, "a") as f:
            if not fileExists:
                f.write("ISO Path,Disk Path,RAM (GB),CPU (Cores)\n")
            f.write(f"{diskPath},{RAM},{CPU},{isoPath}\n")

    def readVMs(self):
        VMs = []
        fileName = "./logs/allVM.txt"
        if os.path.isfile(fileName):
            with open(fileName, "r") as f:
                lines = f.readlines()[1:]
                for line in lines:
                    diskPath, RAM, CPU, isoPath = line.strip().split(",")
                    VMs.append(
                        {
                            "ISO File": isoPath,
                            "Disk Path": diskPath,
                            "RAM (GB)": RAM,
                            "CPU (Cores)": CPU,
                        }
                    )
        return VMs

    def callVM(self, diskPath, requiredRAM, requiredCPU, isoPath):
        """Create a virtual machine if all system requirements (disk, RAM, CPU, ISO file) are met."""
        response = ""
        if diskPath != "" and requiredRAM != "" and requiredCPU != "" and isoPath != "":
            ext, disk = self._checkValidPath(
                diskPath,
                ["qcow2", "vmdk", "vdi", "raw", "vhd"],
            )
            ram = self._checkValidRAM(requiredRAM)
            cpu = self._checkValidCPU(requiredCPU)
            cext, iso = self._checkValidPath(isoPath, ["iso", "img"])
            if disk and ram == True and cpu == True and iso:
                create_virtual_machine(diskPath, requiredRAM, requiredCPU, isoPath)
                self._saveVM(diskPath, requiredRAM, requiredCPU, isoPath)
                return "Creating VM Successfully"
            if not disk:
                response += "Disk Path: " + ext + "\n"
            if ram != True:
                response += "RAM: " + ram + "\n"
            if cpu != True:
                response += "CPU: " + cpu + "\n"
            if not iso:
                response += "ISO Path: " + cext + "\n"
            return response.strip()
        else:
            return "Please Fill out all the information"
