import customtkinter as ctk
from tkinter import messagebox, filedialog
from controller.controllerDocker import DockerController


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


class CreateDockerfilePage:
    def __init__(
        self, root, id=None, file_path=None, file_content=None, description=None
    ):
        self.root = root
        self.edit_mode = file_path is not None
        self.file_path = file_path
        self.window = ctk.CTkToplevel(fg_color="#545454")
        self.window.title("Create Dockerfile")
        self.window.geometry("800x550")
        self.controller = DockerController()

        self.sidebar = ctk.CTkFrame(self.window, width=160, fg_color="white")
        self.sidebar.pack(side="left", fill="y")
        add_sidebar_button(self.sidebar, "Home", self.go_home)
        add_sidebar_button(self.sidebar, "Create Dockerfile", None, disabled=True)
        add_sidebar_button(self.sidebar, "List Dockerfiles", self.go_list_files)
        add_sidebar_button(self.sidebar, "Pull Image from DockerHub", self.go_pull)
        add_sidebar_button(self.sidebar, "Build Docker Image", self.go_build)
        add_sidebar_button(self.sidebar, "Run Docker Image", self.go_run_img)
        add_sidebar_button(self.sidebar, "List Docker Images", self.go_list_imgs)
        add_sidebar_button(self.sidebar, "List Docker Containers", self.go_list_conts)

        self.main_frame = ctk.CTkFrame(self.window, fg_color="#545454")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(
            self.main_frame,
            text="Edit Dockerfile" if self.edit_mode else "Create Dockerfile",
            font=("Segoe UI", 20, "bold"),
            text_color="white",
        ).pack(anchor="w", pady=(0, 20))

        # File path
        ctk.CTkLabel(self.main_frame, text="File Path", text_color="white").pack(
            anchor="w"
        )
        path_frame = ctk.CTkFrame(self.main_frame, fg_color="#545454")
        path_frame.pack(anchor="w", fill="x", pady=6)
        self.path_entry = ctk.CTkEntry(path_frame, width=400)
        self.path_entry.pack(side="left", padx=(0, 10))
        ctk.CTkButton(
            path_frame,
            text="Browse",
            command=self.browse_path,
            width=80,
            fg_color="#004aad",
            hover_color="#444444",
            text_color="white",
        ).pack(side="left")

        # Description area
        ctk.CTkLabel(self.main_frame, text="Description", text_color="white").pack(
            anchor="w", pady=(10, 0)
        )
        self.description_entry = ctk.CTkEntry(self.main_frame, width=600)
        self.description_entry.pack(anchor="w", pady=5)

        # Content area
        code_font = ctk.CTkFont(family="Courier New", size=12)

        ctk.CTkLabel(self.main_frame, text="File Content", text_color="white").pack(
            anchor="w"
        )

        self.content_textbox = ctk.CTkTextbox(
            self.main_frame,
            width=600,
            height=200,
            font=code_font,
            wrap="none",
        )
        self.content_textbox.pack(anchor="w", pady=10)

        if self.edit_mode:
            self.id = id
            self.path_entry.insert(0, file_path)
            self.content_textbox.insert("1.0", file_content)
            if description:
                self.description_entry.insert(0, description)
            button_frame = ctk.CTkFrame(self.main_frame, fg_color="#545454")
            button_frame.pack(anchor="center", pady=20)
            ctk.CTkButton(
                button_frame,
                text="Save Dockerfile",
                command=self.on_edit_click,
                fg_color="green",
                text_color="white",
                width=150,
            ).pack(side="left", padx=10)
            ctk.CTkButton(
                button_frame,
                text="Back",
                command=self.go_home,
                fg_color="red",
                text_color="white",
                width=150,
            ).pack(side="left", padx=10)
        else:
            button_frame = ctk.CTkFrame(self.main_frame, fg_color="#545454")
            button_frame.pack(anchor="center", pady=20)
            ctk.CTkButton(
                button_frame,
                text="Save Dockerfile",
                command=self.on_save_click,
                fg_color="green",
                text_color="white",
                width=150,
            ).pack(side="left", padx=10)
            ctk.CTkButton(
                button_frame,
                text="Back",
                command=self.go_home,
                fg_color="red",
                text_color="white",
                width=150,
            ).pack(side="left", padx=10)

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, path)

    def on_edit_click(self):
        path = self.path_entry.get().strip()
        content = self.content_textbox.get("1.0", "end").strip()
        description = self.description_entry.get().strip()

        success, message = self.controller.EditedDockerFile(
            self.id, path, content, description
        )

        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def on_save_click(self):
        path = self.path_entry.get().strip()
        content = self.content_textbox.get("1.0", "end").strip()
        description = self.description_entry.get().strip()

        success, message = self.controller.saveDockerFile(path, content, description)

        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def go_home(self):
        self.window.destroy()
        self.root.deiconify()

    def go_list_files(self):
        from view.listDKPage import ListDockerfilesPage

        self.window.destroy()
        ListDockerfilesPage(self.root)

    def go_list_imgs(self):
        from view.listImagesPage import ListDockerImagesPage

        self.window.destroy()
        ListDockerImagesPage(self.root)

    def go_pull(self):
        from view.pullDockerImage import DockerImagePullPage

        self.window.destroy()
        DockerImagePullPage(self.root)

    def go_build(self):
        from view.buildDockerImage import BuildDockerImagePage

        self.window.destroy()
        BuildDockerImagePage(self.root)

    def go_run_img(self):
        from view.runImagePage import RunDockerImagePage

        self.window.destroy()
        RunDockerImagePage(self.root)

    def go_list_conts(self):
        from view.listContainersPage import ListRunningContainersPage

        self.window.destroy()
        ListRunningContainersPage(self.root)
