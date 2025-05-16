import webbrowser
import os
import tkinter as tk
from PIL import Image
import customtkinter as ctk
from customtkinter import CTkImage
from view.vdPage import CreateVirtualDiskPage
from view.vmPage import CreateVirtualMachinePage
from view.createDockerFile import CreateDockerfilePage

# Data for virtual machines
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
    (
        "Docker",
        "Docker is a container platform for building, sharing, and running apps.",
        "https://www.youtube.com/watch?v=_dfLOzuIg2o",
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
    elif name.lower() == "docker":
        page = CreateDockerfilePage(root=home_root)

    def on_close():
        page.window.destroy()
        home_root.deiconify()

    page.window.protocol("WM_DELETE_WINDOW", on_close)


def HomePage():
    root = ctk.CTk()
    root.title("Virtual Machines")
    root.geometry("1000x600")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Background image
    bg_image_pil = Image.open(os.path.join("imgs", "newBK.png")).resize((1000, 600))
    root.bg_image = CTkImage(light_image=bg_image_pil, size=(1000, 600))
    bg_label = ctk.CTkLabel(root, image=root.bg_image, text="")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Button styling
    button_font = ctk.CTkFont(size=14, weight="bold")

    for i, order in enumerate(orders_data):
        x = 147 + i * 300
        x2 = 205 + i * 303
        is_vm = order[0].lower() == "virtual machine"
        is_docker = order[0].lower() == "docker"

       # Color sets per type
        if order[0].lower() == "virtual disk":
            start_color = "#e63946"
            start_hover = "#ba1b1d"
            watch_color = "#1d3557"
            hover_watch = "#0d1b2a"
        elif order[0].lower() == "virtual machine":
            start_color = "#2a9d8f"
            start_hover = "#21867a"
            watch_color = "#e9c46a"
            hover_watch = "#f4a261"
        elif order[0].lower() == "docker":
            start_color = "#264653"
            start_hover = "#1f343f"
            watch_color = "#00b4d8"
            hover_watch = "#0077b6"


        # Labels
        start_label = (
            "VD" if order[0].lower() == "virtual disk"
            else "VM" if is_vm
            else "DK"
        )

        # Watch Button
        ctk.CTkButton(
            root,
            text="▶ Watch",
            font=button_font,
            command=lambda url=order[2]: open_demo(url),
            fg_color=watch_color,
            hover_color=hover_watch,
            text_color="white",
            corner_radius=20,
            width=80,
            height=35,
            bg_color="transparent"
        ).place(x=x2 - 23, y=310)

        # Start Button
        ctk.CTkButton(
            root,
            text=start_label,
            font=button_font,
            command=lambda name=order[0]: open_vm_window(name, root),
            fg_color=start_color,
            hover_color=start_hover,
            text_color="white",
            corner_radius=20,
            width=50,
            height=35,
            bg_color="transparent"
        ).place(x=x - 20, y=310)

    root.mainloop()


if __name__ == "__main__":
    HomePage()
