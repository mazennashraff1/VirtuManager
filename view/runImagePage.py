import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
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


class RunDockerImagePage:
    def __init__(self, root, container=None):
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#545454")
        self.window.title("Run Docker Image")
        self.window.geometry("600x400")
        self.controller = DockerController()

        # Sidebar
        self.sidebar = ctk.CTkFrame(self.window, width=160, fg_color="white")
        self.sidebar.pack(side="left", fill="y")
        add_sidebar_button(self.sidebar, "Home", self.go_home)
        add_sidebar_button(self.sidebar, "Run Docker Image", None, disabled=True)

        # Main frame
        self.main_frame = ctk.CTkFrame(self.window, fg_color="#545454")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=40, pady=30)

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

        # Run button
        ctk.CTkButton(
            self.main_frame,
            text="Run Image",
            command=self.on_run_click,
            fg_color="#004aad",
            text_color="white",
            width=150,
        ).pack(anchor="center", pady=20)

        # If container info is passed, fill entries
        if container:
            self.fill_fields(container)

        # Protocol to handle window closing (to restore parent window)
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def fill_fields(self, container):
        self.image_name_entry.delete(0, tk.END)
        self.image_name_entry.insert(0, container.get("Image", ""))

        # Container name optional: you can pre-fill with container name or leave blank
        self.container_name_entry.delete(0, tk.END)
        self.container_name_entry.insert(0, container.get("Name", ""))

    def on_run_click(self):
        image_name = self.image_name_entry.get().strip()
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

        # Auto-generate container name if empty
        if not container_name:
            container_name = (
                f"{image_name.replace(':', '_').replace('/', '_')}_container"
            )

        # Call the controller to run the container
        success, message = self.controller.runDockerImage(
            image_name,
            container_name,
            host_port,
            container_port,
        )

        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def go_home(self):
        self.window.destroy()
        self.root.deiconify()

    def on_close(self):
        self.window.destroy()
        self.root.deiconify()
