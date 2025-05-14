# view/listVDPage.py

import customtkinter as ctk
from controller.controllerVD import VirtualDiskController
import tkinter.messagebox as messagebox


class ListVirtualDisksPage:
    def __init__(self, root):
        self.root = root
        self.controller = VirtualDiskController()
        self.window = ctk.CTkToplevel(fg_color="#545454")
        self.window.title("List All Virtual Disks")
        self.window.geometry("800x500")

        ctk.CTkLabel(
            self.window,
            text="All Virtual Disks",
            font=("Segoe UI", 18, "bold"),
            text_color="white",
        ).pack(pady=20)

        scroll_frame = ctk.CTkScrollableFrame(self.window, fg_color="#545454")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        headers = ["Disk Path", "File Name", "Format", "Size (GB)", "Action", "Delete"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                scroll_frame,
                text=header,
                font=("Segoe UI", 14, "bold"),
                text_color="white",
                width=120,
            ).grid(row=0, column=col, padx=5, pady=5)

        try:
            with open("logs/allVD.txt", "r") as file:
                lines = file.readlines()

            for i, line in enumerate(lines, start=1):
                parts = line.strip().split(",")
                if len(parts) != 4:
                    continue

                path, file_name, format_, size = parts

                ctk.CTkLabel(
                    scroll_frame, text=path, text_color="white", width=120
                ).grid(row=i, column=0, padx=5, pady=5)
                ctk.CTkLabel(
                    scroll_frame, text=file_name, text_color="white", width=120
                ).grid(row=i, column=1, padx=5, pady=5)
                ctk.CTkLabel(
                    scroll_frame, text=format_, text_color="white", width=120
                ).grid(row=i, column=2, padx=5, pady=5)
                ctk.CTkLabel(
                    scroll_frame, text=size, text_color="white", width=120
                ).grid(row=i, column=3, padx=5, pady=5)

                ctk.CTkButton(
                    scroll_frame,
                    text="Edit",
                    fg_color="#004aad",
                    text_color="white",
                    width=80,
                    command=lambda p=path, f=file_name, fm=format_, s=size: self.edit_disk(
                        p, f, fm, s
                    ),
                ).grid(row=i, column=4, padx=5, pady=5)

                ctk.CTkButton(
                    scroll_frame,
                    text="Delete",
                    fg_color="red",
                    text_color="white",
                    width=80,
                    command=lambda f=file_name: self.delete_disk(f),
                ).grid(row=i, column=5, padx=5, pady=5)

        except FileNotFoundError:
            ctk.CTkLabel(
                self.window, text="Error: allVD.txt not found", text_color="red"
            ).pack(pady=10)

    def edit_disk(self, path, file_name, format_, size):
        from view.vdPage import CreateVirtualDiskPage

        self.window.destroy()
        CreateVirtualDiskPage(self.root, disk_data=(path, file_name, format_, size))

    def delete_disk(self, file_name):
        confirm = messagebox.askyesno(
            "Confirm Delete", f"Are you sure you want to delete '{file_name}'?"
        )
        if confirm:
            result = self.controller.deleteVD(file_name)
            messagebox.showinfo("Delete Result", result)
            self.window.destroy()
            ListVirtualDisksPage(self.root)  # Refresh the list
