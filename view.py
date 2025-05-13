import webbrowser
from PIL import Image
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from controller import Controller
from customtkinter import CTkImage
import tkinter.messagebox as messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ---------- Sidebar Button (Reusable) ---------- #
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


# ---------- Virtual Disk Page ---------- #
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
        controller = Controller()
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
        self.window.destroy()
        CreateVirtualMachinePage(self.root)


# ---------- Virtual Machine Page ---------- #
class CreateVirtualMachinePage:
    def __init__(self, root):
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#545454")
        self.window.title("Create Virtual Machine")
        self.window.geometry("800x500")

        self.sidebar = ctk.CTkFrame(self.window, width=160, fg_color="white")
        self.sidebar.pack(side="left", fill="y")
        add_sidebar_button(self.sidebar, "Home", self.go_home)
        add_sidebar_button(self.sidebar, "Create Disk", self.go_vdisk)
        add_sidebar_button(self.sidebar, "Create VM", None, disabled=True)

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
        controller = Controller()
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
        self.window.destroy()
        CreateVirtualDiskPage(self.root)


# ---------- Home Page ---------- #
orders_data = [
    (
        "Virtual Disk",
        "A Virtual Disk emulates a physical disk drive.",
        "https://www.youtube.com/watch?v=tTBt7_aACPI&t=14s",
    ),
    (
        "Virtual Machine",
        "A Virtual Machine emulates a full computer system.",
        "https://www.youtube.com/watch?v=mQP0wqNT_DI",
    ),
]


def open_demo(url):
    webbrowser.open(url)


def open_vm_window(name, home_root):
    home_root.withdraw()
    if name.lower() == "virtual disk":
        page = CreateVirtualDiskPage(home_root)
    elif name.lower() == "virtual machine":
        page = CreateVirtualMachinePage(home_root)

    def on_close():
        page.window.destroy()
        home_root.deiconify()

    page.window.protocol("WM_DELETE_WINDOW", on_close)


def HomePage():
    root = ctk.CTk()
    root.title("Virtual Machines")
    root.geometry("1000x600")

    bg_image_pil = Image.open("Virtual Manager.png").resize((1000, 600))
    root.bg_image = CTkImage(light_image=bg_image_pil, size=(1000, 600))
    bg_label = ctk.CTkLabel(root, image=root.bg_image, text="")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    x_positions = [30, 200, 310, 310]
    for i, order in enumerate(orders_data):
        x = 134 + i * 433
        x2 = 286 + i * 433
        watch_color = "#fec801" if order[0] == "Virtual Machine" else "#004aad"

        ctk.CTkButton(
            root,
            text="Watch",
            command=lambda url=order[2]: open_demo(url),
            fg_color=watch_color,
            hover_color="#e76f51",
            text_color="white",
        ).place(x=x2, y=x_positions[2])

        start_label = "Start VD" if order[0].lower() == "virtual disk" else "Start VM"
        ctk.CTkButton(
            root,
            text=start_label,
            command=lambda name=order[0]: open_vm_window(name, root),
            fg_color="#ff3131",
            hover_color="#21867a",
            text_color="white",
        ).place(x=x, y=x_positions[3])

    root.mainloop()


# Run the home page
HomePage()
