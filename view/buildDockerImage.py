import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from controller.controllerDocker import DockerController
import threading
import time


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


class BuildDockerImagePage:
    def __init__(self, root):
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#545454")
        self.window.title("Build Docker Image")
        self.window.geometry("800x500")
        self.controller = DockerController()

        self.sidebar = ctk.CTkFrame(self.window, width=160, fg_color="white")
        self.sidebar.pack(side="left", fill="y")
        add_sidebar_button(self.sidebar, "Create Dockerfile", self.go_create_file)
        add_sidebar_button(self.sidebar, "Build Docker Image", None, disabled=True)

        self.main_frame = ctk.CTkFrame(self.window, fg_color="#545454")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(
            self.main_frame,
            text="Build Docker Image",
            font=("Segoe UI", 20, "bold"),
            text_color="white",
        ).pack(anchor="w", pady=(0, 20))

        self.image_name = self.add_input("Image Name")
        self.image_tag = self.add_input("Image Tag")
        self.dockerfile_path = self.add_input("Path to Dockerfile", self.browse_file)
        self.build_path = self.add_input("Build Path", self.browse_path)

        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=400)
        self.progress_bar.set(0)

        self.add_buttons(self.build_image, self.back, "Build", "Back")

    def add_input(self, label, browse_command=None):
        ctk.CTkLabel(self.main_frame, text=label, text_color="white").pack(anchor="w")
        frame = ctk.CTkFrame(self.main_frame, fg_color="#545454")
        frame.pack(anchor="w", fill="x", pady=6)
        entry = ctk.CTkEntry(frame, width=320)
        entry.pack(side="left", padx=(0, 10))
        if browse_command:
            ctk.CTkButton(
                frame,
                text="Browse",
                command=browse_command,
                width=80,
                fg_color="#004aad",
                text_color="white",
            ).pack(side="left")
        return entry

    def add_buttons(self, confirm_cmd, cancel_cmd, confirm_text, cancel_text):
        frame = ctk.CTkFrame(self.main_frame, fg_color="#545454")
        frame.pack(anchor="center", pady=20)
        ctk.CTkButton(
            frame,
            text=confirm_text,
            command=confirm_cmd,
            fg_color="green",
            text_color="white",
            width=120,
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            frame,
            text=cancel_text,
            command=cancel_cmd,
            fg_color="red",
            text_color="white",
            width=120,
        ).pack(side="left", padx=10)

    def browse_file(self):
        path = filedialog.askopenfilename(
            title="Select Dockerfile", filetypes=[("Dockerfile", "Dockerfile")]
        )
        if path:
            self.dockerfile_path.delete(0, "end")
            self.dockerfile_path.insert(0, path)

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.build_path.delete(0, "end")
            self.build_path.insert(0, path)

    def build_image(self):
        name = self.image_name.get()
        tag = self.image_tag.get()
        dockerfile = self.dockerfile_path.get()
        build_dir = self.build_path.get()

        # Show and reset progress bar
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)

        def run_build():
            # Simulate progress while building
            progress = 0.0
            while progress < 0.95:
                progress += 0.01
                try:
                    self.window.after(0, lambda p=progress: self.progress_bar.set(p))
                    time.sleep(0.05)
                except:
                    break

            success, message = self.controller.buildDockerImage(
                name, tag, dockerfile, build_dir
            )

            # Set progress to 100%
            self.window.after(0, lambda: self.progress_bar.set(1.0))
            time.sleep(0.5)
            self.window.after(0, self.progress_bar.pack_forget)

            if success:
                self.window.after(0, lambda: messagebox.showinfo("Success", message))
            else:
                self.window.after(
                    0, lambda: messagebox.showerror("Build Failed", message)
                )

        threading.Thread(target=run_build, daemon=True).start()

    def back(self):
        self.window.destroy()
        self.root.deiconify()

    def go_create_file(self):
        self.window.destroy()
        from view.createDockerFile import CreateDockerfilePage

        CreateDockerfilePage(self.root)
