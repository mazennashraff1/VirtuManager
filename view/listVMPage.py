import customtkinter as ctk
from controller.controllerVM import VirtualMachineController


class ListVirtualMachinesPage:
    def __init__(self, root):
        self.root = root
        self.controller = VirtualMachineController()
        self.window = ctk.CTkToplevel(fg_color="#1e1e1e")
        self.window.title("List Virtual Machines")
        self.window.geometry("860x540")
        self.window.protocol("WM_DELETE_WINDOW", self.go_back)

        # --- Back Button ---
        ctk.CTkButton(
            self.window,
            text="← Back",
            command=self.go_back,
            fg_color="#8a1f1f",
            hover_color="#c0392b",
            text_color="white",
            corner_radius=8,
            width=100,
            height=35
        ).pack(anchor="nw", pady=15, padx=20)

        # --- Title ---
        ctk.CTkLabel(
            self.window,
            text="🖥 All Virtual Machines",
            font=("Segoe UI", 22, "bold"),
            text_color="white",
        ).pack(pady=(0, 10), anchor="w", padx=30)

        # --- Scrollable Table ---
        scroll_frame = ctk.CTkScrollableFrame(self.window, fg_color="#1e1e1e", height=400)
        scroll_frame.pack(fill="both", expand=True, padx=30, pady=10)

        headers = ["ISO File", "Disk", "Memory", "CPU", "Action"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                scroll_frame,
                text=header,
                font=("Segoe UI", 14, "bold"),
                text_color="#dddddd",
                width=130,
            ).grid(row=0, column=col, padx=10, pady=10, sticky="w")

        VMs = self.controller.readVMs()
        if not VMs:
            ctk.CTkLabel(
                scroll_frame,
                text="⚠️ No virtual machines found.",
                text_color="white",
                font=("Segoe UI", 13)
            ).grid(row=1, column=0, columnspan=5, pady=20)
        else:
            for i, vm in enumerate(VMs, start=1):
                ctk.CTkLabel(
                    scroll_frame, text=vm["ISO File"], text_color="white", width=130
                ).grid(row=i, column=0, padx=10, pady=6, sticky="w")

                ctk.CTkLabel(
                    scroll_frame, text=vm["Disk Path"], text_color="white", width=130
                ).grid(row=i, column=1, padx=10, pady=6, sticky="w")

                ctk.CTkLabel(
                    scroll_frame, text=vm["RAM (GB)"], text_color="white", width=130
                ).grid(row=i, column=2, padx=10, pady=6, sticky="w")

                ctk.CTkLabel(
                    scroll_frame, text=vm["CPU (Cores)"], text_color="white", width=130
                ).grid(row=i, column=3, padx=10, pady=6, sticky="w")

                ctk.CTkButton(
                    scroll_frame,
                    text="▶ Start",
                    command=lambda name=vm["VM Name"]: self.start_vm(name),
                    fg_color="#2ecc71",
                    hover_color="#27ae60",
                    text_color="white",
                    width=80,
                    height=32
                ).grid(row=i, column=4, padx=10, pady=6)

    def start_vm(self, vm_name):
        print(f"Starting VM: {vm_name}")
        # You could add a real execution hook here (os.system or subprocess)

    def go_back(self):
        self.window.destroy()
        self.root.deiconify()
