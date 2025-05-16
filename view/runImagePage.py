import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from controller.controllerDocker import DockerController
import threading
import time


class RunDockerImagePage:
    def __init__(self, root, container=None):
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#1e1e1e")
        self.window.title("Run Docker Image")
        self.window.geometry("800x620")
        self.controller = DockerController()

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
        self.main_frame.pack(fill="both", expand=True, padx=80, pady=20)

        ctk.CTkLabel(
            self.main_frame,
            text="🚀 Run Docker Image",
            font=("Segoe UI", 22, "bold"),
            text_color="white",
        ).pack(anchor="w", pady=(0, 25))

        self.image_name_entry = self.add_input("📦 Docker Image Name *")
        self.image_tag_entry = self.add_input("🔖 Docker Image Tag *")
        self.container_name_entry = self.add_input("🧾 Container Name (optional)")
        self.host_port_entry = self.add_input("🌐 Host Port *", default="8080", width=120)
        self.container_port_entry = self.add_input("🛠 Container Port", default="80", width=120)

        # --- Progress Bar (hidden by default) ---
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=500)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(10, 0))
        self.progress_bar.pack_forget()

        # --- Run Button ---
        ctk.CTkButton(
            self.main_frame,
            text="▶ Run Image",
            command=self.on_run_click,
            fg_color="#004aad",
            hover_color="#003180",
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=200,
            height=45
        ).pack(pady=(30, 10))

        # Pre-fill fields if editing existing container
        if container:
            self.fill_fields(container)

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_input(self, label_text, default="", width=400):
        ctk.CTkLabel(self.main_frame, text=label_text, text_color="white").pack(anchor="w")
        entry = ctk.CTkEntry(self.main_frame, width=width)
        entry.pack(anchor="w", pady=6)
        if default:
            entry.insert(0, default)
        return entry

    def fill_fields(self, container):
        self.image_name_entry.delete(0, tk.END)
        self.image_name_entry.insert(0, container.get("Image", ""))
        self.image_tag_entry.delete(0, tk.END)
        self.image_tag_entry.insert(0, container.get("Tag", ""))
        self.container_name_entry.delete(0, tk.END)
        self.container_name_entry.insert(0, container.get("Name", ""))

    def on_run_click(self):
        image_name = self.image_name_entry.get().strip()
        image_tag = self.image_tag_entry.get().strip()
        container_name = self.container_name_entry.get().strip()
        host_port = self.host_port_entry.get().strip()
        container_port = self.container_port_entry.get().strip() or "80"

        if not image_name:
            messagebox.showerror("Error", "Docker Image Name is required.")
            return

        if not host_port.isdigit() or not container_port.isdigit():
            messagebox.showerror("Error", "Ports must be valid numbers.")
            return

        if not container_name:
            container_name = f"{image_name.replace(':', '_').replace('/', '_')}_container"

        self.progress_bar.set(0.0)
        self.progress_bar.pack(pady=(10, 0))

        def run_docker():
            success, message = self.controller.runDockerImage(
                image_name, image_tag, container_name, host_port, container_port
            )
            self.progress_bar.set(1.0)
            time.sleep(0.5)
            self.progress_bar.pack_forget()
            if success:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)

        def update_progress():
            progress = 0.0
            while threading.active_count() > 2 and progress < 0.95:
                progress += 0.01
                self.progress_bar.set(progress)
                time.sleep(0.1)

        threading.Thread(target=run_docker, daemon=True).start()
        threading.Thread(target=update_progress, daemon=True).start()

    def go_back(self):
        self.window.destroy()
        from view.createDockerFile import CreateDockerfilePage
        CreateDockerfilePage(self.root)

    def on_close(self):
        self.window.destroy()
        self.root.deiconify()
