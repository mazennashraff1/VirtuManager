import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from controller.controllerDocker import DockerController
import threading
import time


class BuildDockerImagePage:
    def __init__(self, root):
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#1e1e1e")
        self.window.title("Build Docker Image")
        self.window.geometry("880x560")
        self.controller = DockerController()

        self.window.protocol("WM_DELETE_WINDOW", self.go_back)


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
        self.main_frame.pack(fill="both", expand=True, padx=70, pady=10)

        ctk.CTkLabel(
            self.main_frame,
            text="🛠 Build Docker Image",
            font=("Segoe UI", 22, "bold"),
            text_color="white"
        ).pack(anchor="w", pady=(0, 25))

        # Inputs
        self.image_name = self.add_input("📦 Image Name")
        self.image_tag = self.add_input("🔖 Image Tag")
        self.dockerfile_path = self.add_input("📄 Path to Dockerfile", self.browse_file)
        self.build_path = self.add_input("📁 Build Context Path", self.browse_path)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=500)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)
        self.progress_bar.pack_forget()

        # Buttons
        self.add_buttons(self.build_image, self.back, "Build Image", "Cancel")

    def add_input(self, label, browse_command=None):
        ctk.CTkLabel(self.main_frame, text=label, text_color="white").pack(anchor="w")
        frame = ctk.CTkFrame(self.main_frame, fg_color="#1e1e1e")
        frame.pack(anchor="w", fill="x", pady=6)
        entry = ctk.CTkEntry(frame, width=360)
        entry.pack(side="left", padx=(0, 10))
        if browse_command:
            ctk.CTkButton(
                frame,
                text="Browse",
                command=browse_command,
                width=90,
                fg_color="#004aad",
                hover_color="#3c5a94",
                text_color="white",
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(side="left")
        return entry

    def add_buttons(self, confirm_cmd, cancel_cmd, confirm_text, cancel_text):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.pack(pady=25)

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

    def browse_file(self):
        path = filedialog.askopenfilename(
            title="Select Dockerfile",
            filetypes=[("Dockerfile", "Dockerfile")]
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

        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        def run_build():
            progress = 0.0
            while progress < 0.95:
                progress += 0.01
                try:
                    self.window.after(0, lambda p=progress: self.progress_bar.set(p))
                    time.sleep(0.05)
                except:
                    break

            success, message = self.controller.buildDockerImage(name, tag, dockerfile, build_dir)

            self.window.after(0, lambda: self.progress_bar.set(1.0))
            time.sleep(0.5)
            self.window.after(0, self.progress_bar.pack_forget)

            if success:
                self.window.after(0, lambda: messagebox.showinfo("Success", message))
            else:
                self.window.after(0, lambda: messagebox.showerror("Build Failed", message))

        threading.Thread(target=run_build, daemon=True).start()

    def back(self):
        self.window.destroy()
        self.root.deiconify()

    def go_create_file(self):
        self.window.destroy()
        from view.createDockerFile import CreateDockerfilePage
        CreateDockerfilePage(self.root)

    def go_back(self):
        self.window.destroy()
        from view.createDockerFile import CreateDockerfilePage
        CreateDockerfilePage(self.root)
