import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from controller.controllerDocker import DockerController


class ListDockerImagesPage:
    def __init__(self, root):
        self.controller = DockerController()
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#545454")
        self.window.title("List Docker Images")
        self.window.geometry("900x500")

        # Back button
        self.back_button = ctk.CTkButton(
            self.window,
            text="Back",
            command=self.go_back,
            fg_color="#004aad",
            hover_color="#003180",
            text_color="white",
            width=100,
        )
        self.back_button.pack(anchor="nw", padx=20, pady=10)

        ctk.CTkLabel(
            self.window,
            text="📦 Docker Images",
            font=("Segoe UI", 20, "bold"),
            text_color="white",
        ).pack(anchor="w", padx=20, pady=10)

        self.image_frame = tk.Frame(self.window, bg="#545454")
        self.image_frame.pack(fill="both", expand=True, padx=20)

        headers = ["Repository", "Tag", "ImageID", "Created", "Size", "Action"]
        for i, header in enumerate(headers):
            tk.Label(
                self.image_frame,
                text=header,
                font=("Segoe UI", 10, "bold"),
                bg="#545454",
                fg="white",
                padx=5,
            ).grid(row=0, column=i, sticky="w")

        self.load_images()

    def load_images(self):
        images = self.controller.getAllImages()

        for i, img in enumerate(images):
            row_index = i + 1
            pady = 10

            tk.Label(
                self.image_frame, text=img["Repository"], bg="#545454", fg="white"
            ).grid(row=row_index, column=0, sticky="w", padx=5, pady=pady)
            tk.Label(self.image_frame, text=img["Tag"], bg="#545454", fg="white").grid(
                row=row_index, column=1, sticky="w", padx=5, pady=pady
            )
            tk.Label(
                self.image_frame, text=img["ImageID"], bg="#545454", fg="white"
            ).grid(row=row_index, column=2, sticky="w", padx=5, pady=pady)
            tk.Label(
                self.image_frame, text=img["Created"], bg="#545454", fg="white"
            ).grid(row=row_index, column=3, sticky="w", padx=5, pady=pady)
            tk.Label(self.image_frame, text=img["Size"], bg="#545454", fg="white").grid(
                row=row_index, column=4, sticky="w", padx=5, pady=pady
            )

            button_frame = tk.Frame(self.image_frame, bg="#545454")
            button_frame.grid(row=row_index, column=5, padx=5, pady=pady)

            # Run button
            ctk.CTkButton(
                button_frame,
                text="Run",
                width=80,
                command=lambda n=img["Repository"], t=img["Tag"]: self.run_image(n, t),
            ).pack(pady=(0, 5))

            # Delete button
            ctk.CTkButton(
                button_frame,
                text="Delete",
                width=80,
                command=lambda id=img["ImageID"]: self.delete_image(id),
            ).pack()

    def delete_image(self, id):
        res, msg = self.controller.deleteImage(id)
        if res:
            messagebox.showinfo(msg)
        else:
            messagebox.showerror(msg)
        self.refresh()

    def run_image(self, name, tag):
        from view.runImagePage import RunDockerImagePage

        cont = {
            "Image": name,
            "Tag": tag,
        }
        self.window.destroy()
        RunDockerImagePage(self.root, cont)

    def refresh(self):
        for widget in self.image_frame.winfo_children():
            widget.destroy()
        self.load_images()

    def go_back(self):
        self.window.destroy()
        self.root.deiconify()
