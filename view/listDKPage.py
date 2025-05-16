import os
import tkinter as tk
import customtkinter as ctk
from controller.controllerDocker import DockerController


class ListDockerfilesPage:
    def __init__(self, root):
        self.controller = DockerController()
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#1e1e1e")
        self.window.title("List Dockerfiles")
        self.window.geometry("900x400")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.dockerfiles = []
        self.selected_file_path = None

        # --- Back Button Only ---
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

        # --- Main Frame ---
        self.main_frame = ctk.CTkFrame(self.window, fg_color="#1e1e1e")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        ctk.CTkLabel(
            self.main_frame,
            text="📄 Dockerfiles List",
            font=("Segoe UI", 20, "bold"),
            text_color="white",
        ).pack(anchor="w", pady=(0, 15))

        # --- Scrollable Table Frame ---
        self.scroll_canvas = tk.Canvas(
            self.main_frame, width=820, height=200, bg="#1e1e1e", highlightthickness=0
        )
        self.scroll_frame = tk.Frame(self.scroll_canvas, bg="#1e1e1e")
        self.scrollbar = tk.Scrollbar(
            self.main_frame, orient="vertical", command=self.scroll_canvas.yview
        )
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scroll_canvas.pack(side="left", fill="x")
        self.scrollbar.pack(side="right", fill="y")
        self.scroll_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.scroll_canvas.configure(
                scrollregion=self.scroll_canvas.bbox("all")
            ),
        )

        # --- Table Headers ---
        headers = ["ID", "File Path", "Description", "Edit"]
        for i, header in enumerate(headers):
            tk.Label(
                self.scroll_frame,
                text=header,
                font=("Segoe UI", 11, "bold"),
                bg="#1e1e1e",
                fg="#ffffff",
                padx=5,
                pady=5,
            ).grid(row=0, column=i, sticky="w")

        self.load_dockerfile_list()

        # --- Text Viewer ---
        ctk.CTkLabel(self.main_frame, text="📄 File Content", text_color="white").pack(anchor="w", pady=(20, 5))

        code_font = ctk.CTkFont(family="Courier New", size=12)
        self.textbox = ctk.CTkTextbox(
            self.main_frame,
            width=800,
            height=200,
            font=code_font,
            wrap="none",
            fg_color="#2c2c2c",
            border_color="#555555",
            border_width=2,
            text_color="white",
        )
        self.textbox.pack(pady=10)
        self.textbox.configure(state="disabled")

    def go_back(self):
        self.window.destroy()
        from view.createDockerFile import CreateDockerfilePage
        CreateDockerfilePage(self.root)


    def on_close(self):
        self.window.destroy()
        self.root.deiconify()

    def load_dockerfile_list(self):
        self.dockerfiles = self.controller.readDockerfiles()

        for i, df in enumerate(self.dockerfiles, start=1):
            id_label = tk.Label(
                self.scroll_frame, text=df["ID"], bg="#1e1e1e", fg="white", padx=4
            )
            id_label.grid(row=i, column=0, sticky="w")

            path_label = tk.Label(
                self.scroll_frame, text=df["Path"], bg="#1e1e1e", fg="white", padx=4
            )
            path_label.grid(row=i, column=1, sticky="w")

            desc_label = tk.Label(
                self.scroll_frame, text=df["desc"], bg="#1e1e1e", fg="white", padx=4
            )
            desc_label.grid(row=i, column=2, sticky="w")

            for widget in (id_label, path_label, desc_label):
                widget.bind(
                    "<Button-1>",
                    lambda e, path=df["Path"]: self.show_dockerfile_content(path),
                )

            edit_button = ctk.CTkButton(
                self.scroll_frame,
                text="Edit",
                width=80,
                fg_color="#004aad",
                hover_color="#3c5a94",
                text_color="white",
                command=lambda id=df["ID"], path=df["Path"], desc=df["desc"]: self.open_edit_page(id, path, desc),
            )
            edit_button.grid(row=i, column=3, padx=5, pady=2)

    def show_dockerfile_content(self, path):
        content = self.controller.getDockerFileContent(path)
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", content)
        self.textbox.configure(state="disabled")

    def open_edit_page(self, id, path, desc):
        from view.createDockerFile import CreateDockerfilePage
        content = self.controller.getDockerFileContent(path)
        self.window.destroy()
        CreateDockerfilePage(self.root, id=id, file_path=path, file_content=content, description=desc)
