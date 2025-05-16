import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
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


class RunDockerImagePage:
    def __init__(self, root, container=None):
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#545454")
        self.window.title("Run Docker Image")
        self.window.geometry("1000x600")
        self.controller = DockerController()

        # Sidebar on the left
        self.sidebar = ctk.CTkFrame(self.window, width=160, fg_color="white")
        self.sidebar.pack(side="left", fill="y")
        add_sidebar_button(self.sidebar, "Home", self.go_home)

        # Container frame on the right to hold main frame and bottom frame
        self.right_container = ctk.CTkFrame(self.window, fg_color="#545454")
        self.right_container.pack(side="right", fill="both", expand=True)

        # Main frame fills most of the space inside right container
        self.main_frame = ctk.CTkFrame(self.right_container, fg_color="#545454")
        self.main_frame.pack(
            side="top", fill="both", expand=True, padx=40, pady=(30, 10)
        )

        ctk.CTkLabel(
            self.main_frame,
            text="Run Docker Image",
            font=("Segoe UI", 20, "bold"),
            text_color="white",
        ).pack(anchor="w", pady=(0, 20))

        # Docker Image Name
        ctk.CTkLabel(
            self.main_frame, text="Docker Image Name *", text_color="white"
        ).pack(anchor="w")
        self.image_name_entry = ctk.CTkEntry(self.main_frame, width=400)
        self.image_name_entry.pack(anchor="w", pady=6)

        # Docker Tag
        ctk.CTkLabel(
            self.main_frame, text="Docker Image Tag *", text_color="white"
        ).pack(anchor="w")
        self.image_tag_entry = ctk.CTkEntry(self.main_frame, width=400)
        self.image_tag_entry.pack(anchor="w", pady=6)

        # Container Name (optional)
        ctk.CTkLabel(
            self.main_frame, text="Container Name (optional)", text_color="white"
        ).pack(anchor="w")
        self.container_name_entry = ctk.CTkEntry(self.main_frame, width=400)
        self.container_name_entry.pack(anchor="w", pady=6)

        # Host Port
        ctk.CTkLabel(self.main_frame, text="Host Port *", text_color="white").pack(
            anchor="w"
        )
        self.host_port_entry = ctk.CTkEntry(self.main_frame, width=100)
        self.host_port_entry.pack(anchor="w", pady=6)
        self.host_port_entry.insert(0, "8080")  # default

        # Container Port (default 80)
        ctk.CTkLabel(self.main_frame, text="Container Port", text_color="white").pack(
            anchor="w"
        )
        self.container_port_entry = ctk.CTkEntry(self.main_frame, width=100)
        self.container_port_entry.pack(anchor="w", pady=6)
        self.container_port_entry.insert(0, "80")  # default

        # Progress bar (initially hidden)
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(10, 0))
        self.progress_bar.pack_forget()

        # Bottom frame for the Run button
        self.bottom_frame = ctk.CTkFrame(
            self.right_container, fg_color="#545454", height=60
        )
        self.bottom_frame.pack(side="bottom", fill="x", padx=40, pady=(0, 20))
        self.bottom_frame.pack_propagate(False)

        # Run button
        ctk.CTkButton(
            self.bottom_frame,
            text="Run Image",
            command=self.on_run_click,
            fg_color="#004aad",
            text_color="white",
            width=150,
        ).pack(expand=True)

        # If container info is passed, fill entries
        if container:
            self.fill_fields(container)

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

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
            messagebox.showerror(
                "Error", "Host Port and Container Port must be valid numbers."
            )
            return

        if not container_name:
            container_name = (
                f"{image_name.replace(':', '_').replace('/', '_')}_container"
            )

        self.progress_bar.set(0.0)
        self.progress_bar.pack(pady=(10, 0))

        def run_docker():
            success, message = self.controller.runDockerImage(
                image_name,
                image_tag,
                container_name,
                host_port,
                container_port,
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

    def go_home(self):
        self.window.destroy()
        self.root.deiconify()

    def on_close(self):
        self.window.destroy()
        self.root.deiconify()
