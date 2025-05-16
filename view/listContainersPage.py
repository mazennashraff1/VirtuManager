import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from controller.controllerDocker import DockerController


class ListRunningContainersPage:
    def __init__(self, root):
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#545454")
        self.window.title("Running Containers")
        self.window.geometry("900x500")
        self.controller = DockerController()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Back button
        self.back_button = ctk.CTkButton(
            self.window,
            text="Back",
            command=self.go_back,
            fg_color="#004aad",
            hover_color="#003180",
            text_color="white",
            width=100,
        )
        self.back_button.pack(anchor="nw", padx=20, pady=10)

        ctk.CTkLabel(
            self.window,
            text="🟢 Running Containers",
            font=("Segoe UI", 20, "bold"),
            text_color="white",
        ).pack(anchor="w", padx=20, pady=10)

        self.container_frame = ctk.CTkFrame(self.window, fg_color="#545454")
        self.container_frame.pack(fill="both", expand=True, padx=20)

        self.create_headers()

        self.load_containers()

    def create_headers(self):
        headers = ["ID", "Name", "Status", "Image", "Action"]
        for i, header in enumerate(headers):
            tk.Label(
                self.container_frame,
                text=header,
                font=("Segoe UI", 10, "bold"),
                bg="#545454",
                fg="white",
                padx=5,
            ).grid(row=0, column=i, sticky="w")

    def load_containers(self):
        containers = self.controller.getAllContainers()
        for i, cont in enumerate(containers):
            tk.Label(
                self.container_frame, text=cont["ID"], bg="#545454", fg="white"
            ).grid(row=i + 1, column=0, sticky="w", padx=5, pady=3)
            tk.Label(
                self.container_frame, text=cont["Name"], bg="#545454", fg="white"
            ).grid(row=i + 1, column=1, sticky="w", padx=5)
            tk.Label(
                self.container_frame, text=cont["Status"], bg="#545454", fg="white"
            ).grid(row=i + 1, column=2, sticky="w", padx=5)
            tk.Label(
                self.container_frame, text=cont["Image"], bg="#545454", fg="white"
            ).grid(row=i + 1, column=3, sticky="w", padx=5)
            action_text = "Stop" if cont["Running"] else "Run"
            is_running = cont["Running"]
            action_command = lambda c_id=cont["ID"], running=is_running: (
                self.stop_container(c_id) if running else self.run_container(c_id)
            )
            ctk.CTkButton(
                self.container_frame, text=action_text, width=80, command=action_command
            ).grid(row=i + 1, column=4, padx=5)

    def run_container(self, id):
        res, msg = self.controller.startContainer(id)
        if res:
            messagebox.showinfo("Info", msg)
        else:
            messagebox.showerror("Error", msg)
        self.refresh()

    def stop_container(self, container_id):
        res, msg = self.controller.stopContainer(container_id)
        if res:
            messagebox.showinfo("Info", msg)
        else:
            messagebox.showerror("Error", msg)
        self.refresh()

    def refresh(self):
        for widget in self.container_frame.winfo_children():
            widget.destroy()
        self.create_headers()
        self.load_containers()

    def go_back(self):
        self.window.destroy()
        self.root.deiconify()

    def on_close(self):
        self.window.destroy()
        self.root.deiconify()
