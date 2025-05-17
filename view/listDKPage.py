import customtkinter as ctk
import tkinter.messagebox as messagebox
from controller.controllerDocker import DockerController


class ListDockerfilesPage:
    def __init__(self, root):
        self.controller = DockerController()
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#1e1e1e")
        self.window.title("List Dockerfiles")
        self.window.geometry("1000x700")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

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
            height=35,
        ).pack(anchor="nw", pady=15, padx=20)

        # --- Title ---
        ctk.CTkLabel(
            self.window,
            text="📄 Dockerfiles List",
            font=("Segoe UI", 22, "bold"),
            text_color="white",
        ).pack(pady=(10, 10))

        # --- Scrollable Table Container ---
        scroll_frame = ctk.CTkScrollableFrame(
            self.window,
            fg_color="#1e1e1e",
            border_color="#2a2a2a",
            border_width=1,
            height=250,
        )
        scroll_frame.pack(fill="x", expand=False, padx=30, pady=(0, 10))

        # --- Table Headers ---
        headers = ["🆔 ID", "📁 File Path", "📝 Description", "✏️ Edit"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                scroll_frame,
                text=header,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="white",
                width=200 if col == 1 else 120,
            ).grid(row=0, column=col, padx=6, pady=8)

        # --- Table Rows ---
        dockerfiles = self.controller.readDockerfiles()
        if not dockerfiles:
            ctk.CTkLabel(
                scroll_frame,
                text="No Dockerfiles found.",
                text_color="white",
                font=ctk.CTkFont(size=14),
            ).grid(row=1, column=0, columnspan=4, pady=20)
        else:
            for i, df in enumerate(dockerfiles, start=1):
                df_id = df["ID"]
                path = df["Path"]
                desc = df["desc"]

                ctk.CTkLabel(
                    scroll_frame, text=df_id, text_color="white", width=120
                ).grid(row=i, column=0, padx=6, pady=5)
                path_label = ctk.CTkLabel(
                    scroll_frame, text=path, text_color="white", width=200
                )
                path_label.grid(row=i, column=1, padx=6, pady=5)
                desc_label = ctk.CTkLabel(
                    scroll_frame, text=desc, text_color="white", width=200
                )
                desc_label.grid(row=i, column=2, padx=6, pady=5)

                for widget in (path_label, desc_label):
                    widget.bind(
                        "<Button-1>",
                        lambda e, p=path: self.show_dockerfile_content(p),
                    )

                ctk.CTkButton(
                    scroll_frame,
                    text="Edit",
                    fg_color="#004aad",
                    hover_color="#005ce6",
                    text_color="white",
                    width=80,
                    height=32,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    command=lambda i=df_id, p=path, d=desc: self.open_edit_page(
                        i, p, d
                    ),
                ).grid(row=i, column=3, padx=6, pady=5)

        # --- File Viewer Title ---
        ctk.CTkLabel(
            self.window,
            text="📂 Selected Dockerfile Content",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white",
        ).pack(anchor="w", padx=30, pady=(10, 5))

        # --- File Viewer (Textbox) ---
        code_font = ctk.CTkFont(family="Courier New", size=12)
        self.textbox = ctk.CTkTextbox(
            self.window,
            width=920,
            height=250,
            font=code_font,
            wrap="none",
            fg_color="#2c2c2c",
            border_color="#555555",
            border_width=2,
            text_color="white",
        )
        self.textbox.pack(padx=30, pady=(0, 20))
        self.textbox.configure(state="disabled")

    def go_back(self):
        self.window.destroy()
        from view.createDockerFile import CreateDockerfilePage

        CreateDockerfilePage(self.root)

    def on_close(self):
        self.window.destroy()
        self.root.deiconify()

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
        CreateDockerfilePage(
            self.root, id=id, file_path=path, file_content=content, description=desc
        )
