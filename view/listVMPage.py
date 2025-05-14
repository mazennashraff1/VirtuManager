import customtkinter as ctk
from controller.controllerVM import VirtualMachineController  # corrected import


class ListVirtualMachinesPage:
    def __init__(self, root):
        self.root = root
        self.controller = VirtualMachineController()  # use the controller
        self.window = ctk.CTkToplevel(fg_color="#545454")
        self.window.title("List Virtual Machines")
        self.window.geometry("800x500")

        ctk.CTkLabel(
            self.window,
            text="All Virtual Machines",
            font=("Segoe UI", 18, "bold"),
            text_color="white",
        ).pack(pady=20)

        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(self.window, fg_color="#545454")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Table headers
        headers = ["ISO File", "Disk", "Memory", "CPU", "Action"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                scroll_frame,
                text=header,
                font=("Segoe UI", 14, "bold"),
                text_color="white",
                width=120,
            ).grid(row=0, column=col, padx=5, pady=5)

        # Load data via controller
        VMs = self.controller.readVMs()
        if not VMs:
            ctk.CTkLabel(
                self.window, text="No virtual machines found.", text_color="white"
            ).pack(pady=10)
        else:
            for i, vm in enumerate(VMs, start=1):
                ctk.CTkLabel(
                    scroll_frame, text=vm["ISO File"], text_color="white", width=120
                ).grid(row=i, column=0, padx=5, pady=5)
                ctk.CTkLabel(
                    scroll_frame, text=vm["Disk Path"], text_color="white", width=120
                ).grid(row=i, column=1, padx=5, pady=5)
                ctk.CTkLabel(
                    scroll_frame, text=vm["RAM (GB)"], text_color="white", width=120
                ).grid(row=i, column=2, padx=5, pady=5)
                ctk.CTkLabel(
                    scroll_frame, text=vm["CPU (Cores)"], text_color="white", width=120
                ).grid(row=i, column=3, padx=5, pady=5)

                ctk.CTkButton(
                    scroll_frame,
                    text="Start",
                    command=lambda name=vm["VM Name"]: self.start_vm(name),
                    fg_color="#228B22",
                    text_color="white",
                    width=80,
                ).grid(row=i, column=4, padx=5, pady=5)

    def start_vm(self, vm_name):
        print(f"Starting VM: {vm_name}")
