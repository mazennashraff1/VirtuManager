import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from controller.controllerVM import VirtualMachineController
from view.listVMPage import ListVirtualMachinesPage


class CreateVirtualMachinePage:
    def __init__(self, root):
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#1e1e1e")
        self.window.title("Create Virtual Machine")
        self.window.geometry("820x520")

        # --- Top Navigation Bar: Home + List Left, Create VM Right ---
        navbar = ctk.CTkFrame(self.window, fg_color="#1a1a1a", height=70)
        navbar.pack(fill="x", side="top")

        # Left-aligned buttons
        left_buttons = [
            {"icon": "🏠", "label": "Home", "command": self.go_home},
            {"icon": "📋", "label": "List", "command": self.go_list_vms},
        ]

        for btn in left_buttons:
            frame = ctk.CTkFrame(navbar, fg_color="transparent")
            frame.pack(side="left", padx=16, pady=10)

            ctk.CTkLabel(
                frame, text=btn["icon"], font=ctk.CTkFont(size=20), text_color="#cccccc"
            ).pack()

            ctk.CTkButton(
                frame,
                text=btn["label"],
                command=btn["command"],
                fg_color="transparent",
                hover_color="#5c1e1e",
                text_color="#cccccc",
                font=ctk.CTkFont(size=12, weight="bold"),
                width=70,
                height=26
            ).pack()

        # Spacer to push Create VM to the right
        ctk.CTkLabel(navbar, text="", width=400).pack(side="left", expand=True)

        # Right-aligned Create VM (active tab)
        create_frame = ctk.CTkFrame(navbar, fg_color="#2a2a2a", corner_radius=10)
        create_frame.pack(side="right", padx=16, pady=10)

        ctk.CTkLabel(
            create_frame, text="🛠", font=ctk.CTkFont(size=22), text_color="#ff4c4c"
        ).pack()

        ctk.CTkLabel(
            create_frame, text="Create VM", font=ctk.CTkFont(size=12, weight="bold"), text_color="#ff4c4c"
        ).pack()






        # --- Main Content ---
        self.main_frame = ctk.CTkFrame(self.window, fg_color="#1e1e1e")
        self.main_frame.pack(expand=True)

        ctk.CTkLabel(
            self.main_frame,
            text="Create Virtual Machine",
            font=("Segoe UI", 22, "bold"),
            text_color="white"
        ).pack(pady=(25, 15))

       # --- Form (Grid Layout Aligned) ---
        form_grid_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        form_grid_frame.pack()

        self.disk_path = self.add_input_grid(form_grid_frame, 0, "💽 Disk Path:", self.browse_disk_path)
        self.memory = self.add_input_grid(form_grid_frame, 1, "🧠 Memory (GB):")
        self.cpus = self.add_input_grid(form_grid_frame, 2, "🧩 CPUs:")
        self.iso_path = self.add_input_grid(form_grid_frame, 3, "📀 ISO Path:", self.browse_iso_path)

        # Buttons centered below
        self.add_button_row(self.main_frame, self.create_vm, self.back, "✅ Create VM", "↩ Back")

    def add_input_grid(self, parent, row, label_text, browse_command=None, default=""):
        label = ctk.CTkLabel(parent, text=label_text, text_color="white", width=120, anchor="w")
        label.grid(row=row, column=0, padx=(0, 10), pady=8, sticky="e")

        entry = ctk.CTkEntry(parent, width=320)
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=(0, 10), pady=8, sticky="w")

        if browse_command:
            browse_btn = ctk.CTkButton(
                parent,
                text="Browse",
                command=browse_command,
                width=80,
                fg_color="#004aad",
                hover_color="#3c5a94",
                text_color="white"
            )
            browse_btn.grid(row=row, column=2, padx=(0, 10), pady=8, sticky="w")

        return entry



    def add_button_row(self, parent, confirm_cmd, cancel_cmd, confirm_text, cancel_text):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(pady=30)

        ctk.CTkButton(
            frame,
            text=confirm_text,
            command=confirm_cmd,
            fg_color="#1f8a53",
            hover_color="#27ae60",
            text_color="white",
            width=180,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=15)

        ctk.CTkButton(
            frame,
            text=cancel_text,
            command=cancel_cmd,
            fg_color="#8a1f1f",
            hover_color="#c0392b",
            text_color="white",
            width=180,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=15)


    def browse_disk_path(self):
        path = filedialog.askopenfilename(title="Select Virtual Disk File")
        if path:
            self.disk_path.delete(0, "end")
            self.disk_path.insert(0, path)

    def browse_iso_path(self):
        path = filedialog.askopenfilename(title="Select ISO File")
        if path:
            self.iso_path.delete(0, "end")
            self.iso_path.insert(0, path)

    def create_vm(self):
        controller = VirtualMachineController()
        result = controller.callVM(
            self.disk_path.get(),
            self.memory.get(),
            self.cpus.get(),
            self.iso_path.get(),
        )
        messagebox.showinfo("Operation Result", result)

    def back(self):
        self.window.destroy()
        self.root.deiconify()

    def go_home(self):
        self.back()

    def go_list_vms(self):
        self.window.withdraw()
        page = ListVirtualMachinesPage(self.window)

        def on_close():
            page.window.destroy()
            self.window.deiconify()

        page.window.protocol("WM_DELETE_WINDOW", on_close)
