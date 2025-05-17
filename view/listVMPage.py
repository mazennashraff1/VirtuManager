import customtkinter as ctk
from customtkinter import CTkOptionMenu, StringVar
from controller.controllerVM import VirtualMachineController, create_virtual_machine
from model.vm import stop_vm_by_disk_path, is_process_running

class ListVirtualMachinesPage:
    def __init__(self, root):
        self.root = root
        self.controller = VirtualMachineController()
        self.window = ctk.CTkToplevel(fg_color="#1e1e1e")
        self.window.title("List Virtual Machines")
        self.window.geometry("1000x600")
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
        scroll_frame = ctk.CTkScrollableFrame(self.window, fg_color="#1e1e1e", height=300)
        scroll_frame.pack(fill="both", expand=True, padx=30, pady=10)

        headers = ["ISO File", "Disk", "Memory", "CPU"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                scroll_frame,
                text=header,
                font=("Segoe UI", 14, "bold"),
                text_color="#dddddd",
                width=130,
            ).grid(row=0, column=col, padx=10, pady=10, sticky="w")

        self.VMs = self.controller.readVMs()
        if not self.VMs:
            ctk.CTkLabel(
                scroll_frame,
                text="⚠️ No virtual machines found.",
                text_color="white",
                font=("Segoe UI", 13)
            ).grid(row=1, column=0, columnspan=6, pady=20)
        else:
            for i, vm in enumerate(self.VMs, start=1):
                ctk.CTkLabel(scroll_frame, text=vm["ISO File"], text_color="white", width=130).grid(row=i, column=0, padx=10, pady=6, sticky="w")
                ctk.CTkLabel(scroll_frame, text=vm["Disk Path"], text_color="white", width=130).grid(row=i, column=1, padx=10, pady=6, sticky="w")
                ctk.CTkLabel(scroll_frame, text=vm["RAM (GB)"], text_color="white", width=130).grid(row=i, column=2, padx=10, pady=6, sticky="w")
                ctk.CTkLabel(scroll_frame, text=vm["CPU (Cores)"], text_color="white", width=130).grid(row=i, column=3, padx=10, pady=6, sticky="w")

        # --- VM Selection Dropdown ---
        self.selected_vm_var = StringVar()
        vm_options = [vm["Disk Path"] for vm in self.VMs] if self.VMs else []
        self.selected_vm_var.set(vm_options[0] if vm_options else "")

        if vm_options:
            ctk.CTkLabel(
                self.window,
                text="Select VM:",
                text_color="white",
                font=("Segoe UI", 14, "bold")
            ).pack(pady=(10, 0), anchor="w", padx=30)

            self.vm_selector = CTkOptionMenu(
                self.window,
                values=vm_options,
                variable=self.selected_vm_var,
                fg_color="#2c3e50",
                button_color="#34495e",
                button_hover_color="#3c6382",
                text_color="white",
                width=300
            )
            self.vm_selector.pack(pady=10, padx=30, anchor="w")

            # --- Action Buttons ---
            action_frame = ctk.CTkFrame(self.window, fg_color="transparent")
            action_frame.pack(pady=10, padx=30, anchor="w")

            ctk.CTkButton(
                action_frame,
                text="▶ Start Selected VM",
                command=self.start_selected_vm,
                fg_color="#27ae60",
                hover_color="#1e8449",
                text_color="white",
                width=180
            ).pack(side="left", padx=10)

            ctk.CTkButton(
                action_frame,
                text="⏹ Stop Selected VM",
                command=self.stop_selected_vm,
                fg_color="#c0392b",
                hover_color="#922b21",
                text_color="white",
                width=180
            ).pack(side="left", padx=10)

    def get_selected_vm(self):
        selected_disk = self.selected_vm_var.get()
        for vm in self.VMs:
            if vm["Disk Path"] == selected_disk:
                return vm
        return None

    def start_selected_vm(self):
        vm = self.get_selected_vm()
        if vm:
            self.start_vm(vm)
        else:
            print("No VM selected to start.")

    def stop_selected_vm(self):
        vm = self.get_selected_vm()
        if vm:
            stop_vm_by_disk_path(vm["Disk Path"])
        else:
            print("No VM selected to stop.")

    def start_vm(self, vm):
        try:
            disk_path = vm["Disk Path"]
            memory = int(vm["RAM (GB)"])
            cpu_cores = int(vm["CPU (Cores)"])
            iso_path = vm["ISO File"]

            new_pid = create_virtual_machine(disk_path, memory, cpu_cores, iso_path)
            print(f"Started VM with new PID: {new_pid}")

        except Exception as e:
            print(f"[Start Error] {e}")

    def go_back(self):
        self.window.destroy()
        self.root.deiconify()