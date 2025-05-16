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

    bg_image_pil = Image.open(os.path.join("imgs", "all.png")).resize((1000, 600))
    root.bg_image = CTkImage(light_image=bg_image_pil, size=(1000, 600))
    bg_label = ctk.CTkLabel(root, image=root.bg_image, text="")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    x_positions = [30, 200, 190, 190]
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

        start_label = "VD" if order[0].lower() == "virtual disk" else "VM"
        ctk.CTkButton(
            root,
            text=start_label,
            command=lambda name=order[0]: open_vm_window(name, root),
            fg_color="#ff3131",
            hover_color="#21867a",
            text_color="white",
        ).place(x=x, y=x_positions[3])

    second_row_y = [515, 515]
    for i, order in enumerate(orders_data):
        x = 134 + i * 220
        x2 = 286 + i * 220

        watch_color = "#fec801" if order[0].lower() == "docker" else "#004aad"
        if order[0].lower() == "docker":
            watch_color = "#0db7ed"

        start_label = (
            "VD"
            if order[0].lower() == "virtual disk"
            else "VM" if order[0].lower() == "virtual machine" else "DK"
        )

    # Second row - Watch Button
    ctk.CTkButton(
        root,
        text="Watch",
        command=lambda url=order[2]: open_demo(url),
        fg_color=watch_color,
        hover_color="#e76f51",
        text_color="white",
    ).place(x=x2, y=second_row_y[0])

    # Second row - Start Button
    ctk.CTkButton(
        root,
        text=f"{start_label}",
        command=lambda name=order[0]: open_vm_window(name, root),
        fg_color="#ff3131",
        hover_color="#21867a",
        text_color="white",
    ).place(x=x, y=second_row_y[1])
    root.mainloop()


if __name__ == "__main__":
    HomePage()
