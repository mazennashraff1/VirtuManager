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
        fg_color="#2a2a2a" if disabled else "#1f1f1f",
        text_color="#ffffff",
        hover_color="#5c1e1e",
        font=ctk.CTkFont(size=14, weight="bold"),
        height=45,
    ).pack(fill="x", pady=8, padx=12)


class CreateDockerfilePage:
    def __init__(self, root, id=None, file_path=None, file_content=None, description=None):
        self.root = root
        self.edit_mode = file_path is not None
        self.file_path = file_path
        self.window = ctk.CTkToplevel(fg_color="#1e1e1e")
        self.window.title("Create Dockerfile")
        self.window.geometry("900x580")
        self.controller = DockerController()

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self.window, width=160, fg_color="#161616")
        self.sidebar.pack(side="left", fill="y")

        add_sidebar_button(self.sidebar, "🏠 Home", self.go_home)
        add_sidebar_button(self.sidebar, "📝 Create Dockerfile", None, disabled=True)
        add_sidebar_button(self.sidebar, "📄 List Dockerfiles", self.go_list_files)
        add_sidebar_button(self.sidebar, "⬇️ Pull Image", self.go_pull)
        add_sidebar_button(self.sidebar, "⚙️ Build Image", self.go_build)
        add_sidebar_button(self.sidebar, "🚀 Run Image", self.go_run_img)
        add_sidebar_button(self.sidebar, "🗃 Docker Images", self.go_list_imgs)
        add_sidebar_button(self.sidebar, "📦 Containers", self.go_list_conts)
        add_sidebar_button(self.sidebar, "🔍 Search Image", self.go_search_image)

        # --- Main Area ---
        self.main_frame = ctk.CTkFrame(self.window, fg_color="#1e1e1e")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(
            self.main_frame,
            text="Edit Dockerfile" if self.edit_mode else "Create Dockerfile",
            font=("Segoe UI", 22, "bold"),
            text_color="white",
        ).pack(pady=(0, 20))

        # --- Grid Form ---
        form_grid_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        form_grid_frame.pack(anchor="center")

        self.path_entry = self.add_input_grid(form_grid_frame, 0, "📁 File Path:", self.browse_path)
        self.description_entry = self.add_input_grid(form_grid_frame, 1, "📝 Description:")

        # --- Content Box ---
        ctk.CTkLabel(self.main_frame, text="📄 File Content", text_color="white").pack(anchor="w", padx=10, pady=(15, 5))

        code_font = ctk.CTkFont(family="Courier New", size=12)
        self.content_textbox = ctk.CTkTextbox(
            self.main_frame,
            width=600,
            height=200,
            font=code_font,
            wrap="none",
            fg_color="#2c2c2c",       # darker gray background
            border_color="#ff4c4c",   # subtle red border for focus
            border_width=2,
            text_color="white"
        )

        self.content_textbox.pack(anchor="center", pady=10)

        # --- Buttons ---
        self.add_button_row(
            self.main_frame,
            self.on_edit_click if self.edit_mode else self.on_save_click,
            self.go_home,
            "💾 Save Dockerfile",
            "↩ Back"
        )

        # Fill if editing
        if self.edit_mode:
            self.id = id
            self.path_entry.insert(0, file_path)
            self.content_textbox.insert("1.0", file_content)
            if description:
                self.description_entry.insert(0, description)

    def add_input_grid(self, parent, row, label_text, browse_command=None, default=""):
        label = ctk.CTkLabel(parent, text=label_text, text_color="white", width=120, anchor="w")
        label.grid(row=row, column=0, padx=(0, 10), pady=8, sticky="e")

        entry = ctk.CTkEntry(parent, width=400)
        entry.insert(0, default)
        entry.grid(row=row, column=1, padx=(0, 10), pady=8, sticky="w")

        if browse_command:
            ctk.CTkButton(
                parent,
                text="Browse",
                command=browse_command,
                width=80,
                fg_color="#004aad",
                hover_color="#3c5a94",
                text_color="white"
            ).grid(row=row, column=2, padx=(0, 10), pady=8, sticky="w")

        return entry

    def add_button_row(self, parent, confirm_cmd, cancel_cmd, confirm_text, cancel_text):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(pady=30)

        ctk.CTkButton(
            frame,
            text=confirm_text,
            command=confirm_cmd,
            fg_color="#1f8a53",
            hover_color="#27ae60",
            text_color="white",
            width=180,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=15)

        ctk.CTkButton(
            frame,
            text=cancel_text,
            command=cancel_cmd,
            fg_color="#8a1f1f",
            hover_color="#c0392b",
            text_color="white",
            width=180,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=15)

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, path)

    def on_edit_click(self):
        path = self.path_entry.get().strip()
        content = self.content_textbox.get("1.0", "end").strip()
        description = self.description_entry.get().strip()
        success, message = self.controller.EditedDockerFile(self.id, path, content, description)
        messagebox.showinfo("Success" if success else "Error", message)

    def on_save_click(self):
        path = self.path_entry.get().strip()
        content = self.content_textbox.get("1.0", "end").strip()
        description = self.description_entry.get().strip()
        success, message = self.controller.saveDockerFile(path, content, description)
        messagebox.showinfo("Success" if success else "Error", message)

    # --- Navigation ---
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

    def go_search_image(self):
        from view.searchDImagePage import SearchDockerImagePage
        self.window.destroy()
        SearchDockerImagePage(self.root)
