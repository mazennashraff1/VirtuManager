import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from controller.controllerDocker import DockerController
import threading
import time


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

        # Progress bar (initially hidden)
        self.progress_bar = ctk.CTkProgressBar(self.window, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.pack_forget()

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
                self.container_frame,
                text=action_text,
                width=80,
                command=action_command,
            ).grid(row=i + 1, column=4, padx=5)

    def run_container(self, id):
        self.show_progress_bar()

        def action():
            res, msg = self.controller.startContainer(id)
            self.window.after(0, lambda: self.progress_bar.set(1.0))
            time.sleep(0.5)
            self.window.after(0, self.progress_bar.pack_forget)
            self.window.after(
                0,
                lambda: (
                    messagebox.showinfo("Info", msg)
                    if res
                    else messagebox.showerror("Error", msg)
                ),
            )
            if self.window.winfo_exists():
                self.refresh()

        threading.Thread(target=action, daemon=True).start()
        threading.Thread(target=self.progress_loop, daemon=True).start()

    def stop_container(self, container_id):
        self.show_progress_bar()

        def action():
            res, msg = self.controller.stopContainer(container_id)
            self.window.after(0, lambda: self.progress_bar.set(1.0))
            time.sleep(0.5)
            self.window.after(0, self.progress_bar.pack_forget)
            self.window.after(
                0,
                lambda: (
                    messagebox.showinfo("Info", msg)
                    if res
                    else messagebox.showerror("Error", msg)
                ),
            )
            if self.window.winfo_exists():
                self.refresh()

        threading.Thread(target=action, daemon=True).start()
        threading.Thread(target=self.progress_loop, daemon=True).start()

    def progress_loop(self):
        progress = 0.0
        while threading.active_count() > 2 and progress < 0.95:
            progress += 0.01
            try:
                self.window.after(0, lambda p=progress: self.progress_bar.set(p))
            except:
                break
            time.sleep(0.1)

    def show_progress_bar(self):
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(0, 10))

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
