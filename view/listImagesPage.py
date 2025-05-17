import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from controller.controllerDocker import DockerController


class ListDockerImagesPage:
    def __init__(self, root):
        self.controller = DockerController()
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#1e1e1e")
        self.window.title("List Docker Images")
        self.window.geometry("1000x600")

        # Back Button
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

        # Title
        ctk.CTkLabel(
            self.window,
            text="📦 Docker Images",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="white"
        ).pack(anchor="w", padx=30, pady=(0, 10))

        # --- Scrollable Frame Setup ---
        container = ctk.CTkFrame(self.window, fg_color="#1e1e1e")
        container.pack(fill="both", expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container, bg="#1e1e1e", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(container, orientation="vertical", command=canvas.yview)
        self.scroll_frame = ctk.CTkFrame(canvas, fg_color="#1e1e1e")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Table Headers
        headers = ["Repository", "Tag", "ImageID", "Created", "Size", "Action"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                self.scroll_frame,
                text=header,
                text_color="#cccccc",
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w"
            ).grid(row=0, column=i, padx=10, pady=10, sticky="w")

        self.load_images()

    def load_images(self):
        images = self.controller.getAllImages()

        for i, img in enumerate(images):
            row = i + 1
            padding = {"padx": 10, "pady": 5}

            ctk.CTkLabel(self.scroll_frame, text=img["Repository"], text_color="white").grid(row=row, column=0, **padding, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=img["Tag"], text_color="white").grid(row=row, column=1, **padding, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=img["ImageID"], text_color="white").grid(row=row, column=2, **padding, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=img["Created"], text_color="white").grid(row=row, column=3, **padding, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=img["Size"], text_color="white").grid(row=row, column=4, **padding, sticky="w")

            # Actions
            btn_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            btn_frame.grid(row=row, column=5, padx=10, pady=5)

            # Run button
            ctk.CTkButton(
                btn_frame,
                text="▶ Run",
                width=80,
                fg_color="#1f8a53",
                hover_color="#27ae60",
                text_color="white",
                command=lambda n=img["Repository"], t=img["Tag"]: self.run_image(n, t)
            ).pack(side="left", padx=5)

            # Delete button
            ctk.CTkButton(
                btn_frame,
                text="🗑 Delete",
                width=80,
                fg_color="#8a1f1f",
                hover_color="#c0392b",
                text_color="white",
                command=lambda id=img["ImageID"]: self.delete_image(id)
            ).pack(side="left", padx=5)

    def delete_image(self, id):
        res, msg = self.controller.deleteImage(id)
        if res:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)
        self.refresh()

    def run_image(self, name, tag):
        from view.runImagePage import RunDockerImagePage
        cont = {"Image": name, "Tag": tag}
        self.window.destroy()
        RunDockerImagePage(self.root, cont)

    def refresh(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.load_images()

    def go_back(self):
        self.window.destroy()
        from view.createDockerFile import CreateDockerfilePage
        CreateDockerfilePage(self.root)
