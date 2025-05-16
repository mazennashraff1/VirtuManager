import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from controller.controllerVD import VirtualDiskController
from view.listVDPage import ListVirtualDisksPage


class CreateVirtualDiskPage:
    def __init__(self, root, disk_data=None):
        self.root = root
        self.disk_data = disk_data
        self.window = ctk.CTkToplevel(fg_color="#1e1e1e")
        self.window.title("Create Virtual Disk")
        self.window.geometry("820x520")

        # --- Top Navigation Bar ---
        navbar = ctk.CTkFrame(self.window, fg_color="#1a1a1a", height=80)
        navbar.pack(fill="x", side="top")

        # --- Left Buttons ---
        left_buttons = [
            {"icon": "🏠", "label": "Home", "command": self.go_home},
            {"icon": "📋", "label": "List", "command": self.go_list_vd},
        ]
        for btn in left_buttons:
            frame = ctk.CTkFrame(navbar, fg_color="transparent")
            frame.pack(side="left", padx=16, pady=10)
            ctk.CTkLabel(frame, text=btn["icon"], font=ctk.CTkFont(size=22), text_color="#cccccc").pack()
            ctk.CTkButton(
                frame, text=btn["label"], command=btn["command"],
                fg_color="transparent", hover_color="#5c1e1e", text_color="#cccccc",
                font=ctk.CTkFont(size=14, weight="bold"), width=80, height=32
            ).pack()

        # --- Spacer & Active Button Right ---
        ctk.CTkLabel(navbar, text="", width=400).pack(side="left", expand=True)
        create_frame = ctk.CTkFrame(navbar, fg_color="#2a2a2a", corner_radius=10)
        create_frame.pack(side="right", padx=16, pady=10)
        ctk.CTkLabel(create_frame, text="💽", font=ctk.CTkFont(size=24), text_color="#ff4c4c").pack()
        ctk.CTkLabel(create_frame, text=" Create VD ", font=ctk.CTkFont(size=14, weight="bold"), text_color="#ff4c4c").pack()

        # --- Main Form Frame ---
        self.main_frame = ctk.CTkFrame(self.window, fg_color="#1e1e1e")
        self.main_frame.pack(expand=True, pady=30)

        ctk.CTkLabel(
            self.main_frame,
            text="Create Virtual Disk" if not self.disk_data else "Edit Virtual Disk",
            font=("Segoe UI", 22, "bold"),
            text_color="white",
        ).grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # --- Disk Path ---
        ctk.CTkLabel(self.main_frame, text="📂 Disk Path:", text_color="white", anchor="w").grid(row=1, column=0, padx=10, pady=8, sticky="e")
        self.disk_path = ctk.CTkEntry(self.main_frame, width=320)
        self.disk_path.grid(row=1, column=1, padx=10, pady=8)
        ctk.CTkButton(
            self.main_frame, text="Browse", command=self.browse_path,
            width=80, fg_color="#004aad", hover_color="#3c5a94", text_color="white"
        ).grid(row=1, column=2, padx=10, pady=8)

        # --- File Name ---
        ctk.CTkLabel(self.main_frame, text="📝 File Name:", text_color="white", anchor="w").grid(row=2, column=0, padx=10, pady=8, sticky="e")
        self.file_name = ctk.CTkEntry(self.main_frame, width=320)
        self.file_name.grid(row=2, column=1, columnspan=2, padx=10, pady=8, sticky="w")

        # --- Format ---
        ctk.CTkLabel(self.main_frame, text="📦 Format:", text_color="white", anchor="w").grid(row=3, column=0, padx=10, pady=8, sticky="e")
        self.disk_format = ctk.CTkComboBox(self.main_frame, values=["qcow2", "vmdk", "vdi", "raw", "vhd"], width=320)
        self.disk_format.grid(row=3, column=1, columnspan=2, padx=10, pady=8, sticky="w")

        # --- Size ---
        ctk.CTkLabel(self.main_frame, text="💾 Size (GB):", text_color="white", anchor="w").grid(row=4, column=0, padx=10, pady=8, sticky="e")
        self.disk_size = ctk.CTkEntry(self.main_frame, width=320)
        self.disk_size.grid(row=4, column=1, columnspan=2, padx=10, pady=8, sticky="w")
        self.disk_size.insert(0, "1")

        # --- Prefill Data if Edit Mode ---
        if self.disk_data:
            self.disk_path.insert(0, self.disk_data[0])
            self.file_name.insert(0, self.disk_data[1])
            self.disk_format.set(self.disk_data[2])
            self.disk_size.insert(0, self.disk_data[3])

        # --- Buttons ---
        confirm_text = "✅ Save Disk" if self.disk_data else "✅ Create Disk"
        ctk.CTkButton(
            self.main_frame, text=confirm_text,
            command=self.save_disk if self.disk_data else self.create_disk,
            fg_color="#1f8a53", hover_color="#27ae60", text_color="white", width=140
        ).grid(row=5, column=1, padx=10, pady=30, sticky="e")

        ctk.CTkButton(
            self.main_frame, text="↩ Back", command=self.back,
            fg_color="#8a1f1f", hover_color="#c0392b", text_color="white", width=140
        ).grid(row=5, column=2, padx=10, pady=30, sticky="w")

    # --- Utility Functions ---
    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.disk_path.delete(0, "end")
            self.disk_path.insert(0, path)

    def create_disk(self):
        controller = VirtualDiskController()
        result = controller.callVD(
            self.file_name.get(),
            self.disk_path.get(),
            self.disk_format.get(),
            self.disk_size.get(),
        )
        messagebox.showinfo("Operation Result", result)

    def save_disk(self):
        controller = VirtualDiskController()
        result = controller.updateVD(
            self.disk_data[1],
            self.file_name.get(),
            self.disk_path.get(),
            self.disk_format.get(),
            self.disk_size.get(),
        )
        messagebox.showinfo("Operation Result", result)
        self.window.destroy()
        self.root.deiconify()

    def back(self):
        self.window.destroy()
        self.root.deiconify()

    def go_home(self):
        self.back()

    def go_vm(self):
        from vmPage import CreateVirtualMachinePage
        self.window.destroy()
        CreateVirtualMachinePage(self.root)

    def go_list_vd(self):
        from view.listVDPage import ListVirtualDisksPage
        self.window.destroy()
        ListVirtualDisksPage(self.root)
