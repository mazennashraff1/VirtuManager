import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from controller.controllerVD import VirtualDiskController


def add_sidebar_button(parent, text, command, disabled=False):
    state = "disabled" if disabled else "normal"
    ctk.CTkButton(
        parent,
        text=text,
        command=command,
        state=state,
        corner_radius=10,
        fg_color="#545454",
        text_color="white",
        hover_color="#444444",
        height=40,
    ).pack(fill="x", pady=6, padx=10)


class CreateVirtualDiskPage:
    def __init__(self, root):
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#545454")
        self.window.title("Create Virtual Disk")
        self.window.geometry("800x500")

        self.sidebar = ctk.CTkFrame(self.window, width=160, fg_color="white")
        self.sidebar.pack(side="left", fill="y")
        add_sidebar_button(self.sidebar, "Home", self.go_home)
        add_sidebar_button(self.sidebar, "Create Disk", None, disabled=True)
        add_sidebar_button(self.sidebar, "Create VM", self.go_vm)

        self.main_frame = ctk.CTkFrame(self.window, fg_color="#545454")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(
            self.main_frame,
            text="Create Virtual Disk",
            font=("Segoe UI", 20, "bold"),
            text_color="white",
        ).pack(anchor="w", pady=(0, 20))

        self.disk_path = self.add_input("Disk Path", self.browse_path)
        self.file_name = self.add_input("File Name")
        self.disk_format = self.add_combobox(
            "Disk Format",
            ["qcow2", "vmdk", "vdi", "raw", "vhd"],
        )
        self.disk_size = self.add_input("Disk Size (GB)", default="1")

        self.add_button_row(self.create_disk, self.back, "Create Disk", "Back")

    def add_input(self, label, browse_command=None, default=""):
        ctk.CTkLabel(self.main_frame, text=label, text_color="white").pack(anchor="w")
        frame = ctk.CTkFrame(self.main_frame, fg_color="#545454")
        frame.pack(anchor="w", fill="x", pady=6)
        entry = ctk.CTkEntry(frame, width=320)
        entry.insert(0, default)
        entry.pack(side="left", padx=(0, 10))
        if browse_command:
            ctk.CTkButton(
                frame,
                text="Browse",
                command=browse_command,
                width=80,
                fg_color="#004aad",
                hover_color="#444444",
                text_color="white",
            ).pack(side="left")
        return entry

    def add_combobox(self, label, values):
        ctk.CTkLabel(self.main_frame, text=label, text_color="white").pack(
            anchor="w", pady=(10, 0)
        )
        cb = ctk.CTkComboBox(self.main_frame, values=values)
        cb.pack(anchor="w", pady=6)
        return cb

    def add_button_row(self, confirm_cmd, cancel_cmd, confirm_text, cancel_text):
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="#545454")
        button_frame.pack(anchor="center", pady=20)
        ctk.CTkButton(
            button_frame,
            text=confirm_text,
            command=confirm_cmd,
            fg_color="red",
            hover_color="#444444",
            text_color="white",
            width=120,
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            button_frame,
            text=cancel_text,
            command=cancel_cmd,
            fg_color="red",
            hover_color="#444444",
            text_color="white",
            width=120,
        ).pack(side="left", padx=10)

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

    def back(self):
        self.window.destroy()
        self.root.deiconify()

    def go_home(self):
        self.back()

    def go_vm(self):
        from vmPage import CreateVirtualMachinePage

        self.window.destroy()
        CreateVirtualMachinePage(self.root)
