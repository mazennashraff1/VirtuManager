import customtkinter as ctk
import tkinter.messagebox as messagebox
from controller.controllerVD import VirtualDiskController


class ListVirtualDisksPage:
    def __init__(self, root):
        self.root = root
        self.controller = VirtualDiskController()
        self.window = ctk.CTkToplevel(fg_color="#1e1e1e")
        self.window.title("List All Virtual Disks")
        self.window.geometry("820x520")
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
            text="🧾 All Virtual Disks",
            font=("Segoe UI", 22, "bold"),
            text_color="white",
        ).pack(pady=(20, 10))

        # --- Scrollable Table Container ---
        scroll_frame = ctk.CTkScrollableFrame(
            self.window, fg_color="#1e1e1e", border_color="#2a2a2a", border_width=1
        )
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Table Headers ---
        headers = ["📁 Path", "📄 Name", "📦 Format", "💾 Size (GB)", "✏️ Edit", "🗑 Delete"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                scroll_frame,
                text=header,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="white",
                width=120,
            ).grid(row=0, column=col, padx=6, pady=8)

        # --- Table Rows ---
        VDs = self.controller.readVDs()
        if not VDs:
            ctk.CTkLabel(
                scroll_frame,
                text="No virtual disks found.",
                text_color="white",
                font=ctk.CTkFont(size=14)
            ).grid(row=1, column=0, columnspan=6, pady=20)
        else:
            for i, vd in enumerate(VDs, start=1):
                full_path = vd["Disk Path"]
                format_ = vd["Format"]
                size = vd["Size (GB)"]

                file_name = full_path.split("/")[-1]
                dir_path = full_path.rsplit("/", 1)[0]

                # Labels
                ctk.CTkLabel(
                    scroll_frame, text=dir_path, text_color="white", width=120
                ).grid(row=i, column=0, padx=6, pady=5)
                ctk.CTkLabel(
                    scroll_frame, text=file_name, text_color="white", width=120
                ).grid(row=i, column=1, padx=6, pady=5)
                ctk.CTkLabel(
                    scroll_frame, text=format_, text_color="white", width=120
                ).grid(row=i, column=2, padx=6, pady=5)
                ctk.CTkLabel(
                    scroll_frame, text=size, text_color="white", width=120
                ).grid(row=i, column=3, padx=6, pady=5)

                # Edit Button
                ctk.CTkButton(
                    scroll_frame,
                    text="Edit",
                    fg_color="#004aad",
                    hover_color="#005ce6",
                    text_color="white",
                    width=80,
                    height=32,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    command=lambda p=dir_path, f=file_name, fm=format_, s=size: self.edit_disk(
                        p, f, fm, s
                    ),
                ).grid(row=i, column=4, padx=6, pady=5)

                # Delete Button
                ctk.CTkButton(
                    scroll_frame,
                    text="Delete",
                    fg_color="#8a1f1f",
                    hover_color="#c0392b",
                    text_color="white",
                    width=80,
                    height=32,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    command=lambda f=file_name: self.delete_disk(f),
                ).grid(row=i, column=5, padx=6, pady=5)

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
            ListVirtualDisksPage(self.root)
    def go_back(self):
        self.window.destroy()
        self.root.deiconify()