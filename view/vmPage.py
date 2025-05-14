import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from controller.controllerVM import VirtualMachineController
from view.listVMPage import ListVirtualMachinesPage


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


class CreateVirtualMachinePage:
    def __init__(self, root):
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#545454")
        self.window.title("Create Virtual Machine")
        self.window.geometry("800x500")

        self.sidebar = ctk.CTkFrame(self.window, width=160, fg_color="white")
        self.sidebar.pack(side="left", fill="y")
        add_sidebar_button(self.sidebar, "Home", self.go_home)
        add_sidebar_button(self.sidebar, "Create VM", None, disabled=True)
        add_sidebar_button(self.sidebar, "List All VMs", self.go_list_vms)

        self.main_frame = ctk.CTkFrame(self.window, fg_color="#545454")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(
            self.main_frame,
            text="Create Virtual Machine",
            font=("Segoe UI", 20, "bold"),
            text_color="white",
        ).pack(anchor="w", pady=(0, 20))

        self.disk_path = self.add_entry("Disk Path", self.browse_disk_path)
        self.memory = self.add_entry("Memory (GB)")
        self.cpus = self.add_entry("CPUs")
        self.iso_path = self.add_entry("ISO Path", self.browse_iso_path)

        self.add_button_row(self.create_vm, self.back, "Create VM", "Back")

    def add_entry(self, label, browse_cmd=None):
        ctk.CTkLabel(self.main_frame, text=label, text_color="white").pack(anchor="w")
        frame = ctk.CTkFrame(self.main_frame, fg_color="#545454")
        frame.pack(anchor="w", fill="x", pady=6)
        entry = ctk.CTkEntry(frame, width=320)
        entry.pack(side="left", padx=(0, 10))
        if browse_cmd:
            ctk.CTkButton(
                frame,
                text="Browse",
                command=browse_cmd,
                width=80,
                fg_color="#004aad",
                hover_color="#444444",
                text_color="white",
            ).pack(side="left")
        return entry

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

    def go_vdisk(self):
        from vdPage import CreateVirtualDiskPage

        self.window.destroy()
        CreateVirtualDiskPage(self.root)

    def go_list_vms(self):
        self.window.withdraw()
        page = ListVirtualMachinesPage(self.window)

        def on_close():
            page.window.destroy()
            self.window.deiconify()

        page.window.protocol("WM_DELETE_WINDOW", on_close)
