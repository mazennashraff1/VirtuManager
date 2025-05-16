import os
import tkinter as tk
import customtkinter as ctk
from controller.controllerDocker import DockerController


class ListDockerfilesPage:
    def __init__(self, root):
        self.controller = DockerController()
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#545454")
        self.window.title("List Dockerfiles")
        self.window.geometry("900x600")
        self.dockerfiles = self.controller.readDockerfiles()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.dockerfiles = []
        self.selected_file_path = None

        self.sidebar = ctk.CTkFrame(self.window, width=160, fg_color="white")
        self.sidebar.pack(side="left", fill="y")
        ctk.CTkButton(self.sidebar, text="Back", command=self.go_back).pack(
            pady=10, padx=10
        )

        self.main_frame = ctk.CTkFrame(self.window, fg_color="#545454")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            self.main_frame,
            text="📄 Dockerfiles List",
            font=("Segoe UI", 20, "bold"),
            text_color="white",
        ).pack(anchor="w", pady=(0, 10))

        # Scrollable frame for table
        self.scroll_canvas = tk.Canvas(
            self.main_frame, width=700, height=200, bg="#545454", highlightthickness=0
        )
        self.scroll_frame = tk.Frame(self.scroll_canvas, bg="#545454")
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

        # Table headers
        headers = ["ID", "File Path", "Description", "Edit"]
        for i, header in enumerate(headers):
            tk.Label(
                self.scroll_frame,
                text=header,
                font=("Segoe UI", 10, "bold"),
                bg="#545454",
                fg="white",
                padx=5,
            ).grid(row=0, column=i, sticky="w")

        self.load_dockerfile_list()

        # Text editor and button
        code_font = ctk.CTkFont(family="Courier New", size=12)

        ctk.CTkLabel(self.main_frame, text="File Content", text_color="white").pack(
            anchor="w"
        )

        self.textbox = ctk.CTkTextbox(
            self.main_frame,
            width=700,
            height=200,
            font=code_font,
            wrap="none",  # disables word wrap, so lines scroll horizontally
            fg_color="#3a3a3a",
            text_color="white",
        )
        self.textbox.pack(pady=15)

        # Make the textbox read-only
        self.textbox.configure(state="disabled")

    def go_back(self):
        self.window.destroy()
        self.root.deiconify()

    def on_close(self):
        self.window.destroy()
        self.root.deiconify()

    def load_dockerfile_list(self):
        self.dockerfiles = self.controller.readDockerfiles()

        for i, df in enumerate(self.dockerfiles, start=1):
            # Create labels for each column
            id_label = tk.Label(
                self.scroll_frame, text=df["ID"], bg="#545454", fg="white"
            )
            id_label.grid(row=i, column=0, sticky="w", padx=5)

            path_label = tk.Label(
                self.scroll_frame, text=df["Path"], bg="#545454", fg="white"
            )
            path_label.grid(row=i, column=1, sticky="w", padx=5)

            desc_label = tk.Label(
                self.scroll_frame, text=df["desc"], bg="#545454", fg="white"
            )
            desc_label.grid(row=i, column=2, sticky="w", padx=5)

            # Bind click event to labels to show content in textbox
            # Pass the path to the callback via lambda default argument
            for widget in (id_label, path_label, desc_label):
                widget.bind(
                    "<Button-1>",
                    lambda e, path=df["Path"]: self.show_dockerfile_content(path),
                )

            edit_button = ctk.CTkButton(
                self.scroll_frame,
                text="Edit",
                width=80,
                command=lambda id=df["ID"], path=df["Path"], desc=df[
                    "desc"
                ]: self.open_edit_page(id, path, desc),
            )
            edit_button.grid(row=i, column=3, padx=5, pady=2)

    def show_dockerfile_content(self, path):
        # Get the file content
        content = self.controller.getDockerFileContent(path)

        # Enable textbox to update text
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", content)
        # Make textbox read-only again
        self.textbox.configure(state="disabled")

    def open_edit_page(self, id, path, desc):
        from view.createDockerFile import CreateDockerfilePage

        content = self.controller.getDockerFileContent(path)
        self.window.destroy()

        CreateDockerfilePage(
            self.root, id=id, file_path=path, file_content=content, description=desc
        )
