import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from controller.controllerDocker import DockerController
import threading
import time


class ListRunningContainersPage:
    def __init__(self, root):
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#1e1e1e")
        self.window.title("Running Containers")
        self.window.geometry("1000x600")
        self.controller = DockerController()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Back Button
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

        ctk.CTkLabel(
            self.window,
            text="🟢 Running Containers",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="white",
        ).pack(anchor="w", padx=30, pady=(0, 15))

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.window, width=600)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.pack_forget()

        # Scrollable container frame
        container = ctk.CTkFrame(self.window, fg_color="#1e1e1e")
        container.pack(fill="both", expand=True, padx=20)

        canvas = tk.Canvas(container, bg="#1e1e1e", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(
            container, orientation="vertical", command=canvas.yview
        )
        self.scroll_frame = ctk.CTkFrame(canvas, fg_color="#1e1e1e")

        self.scroll_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.create_headers()
        self.load_containers()

    def create_headers(self):
        headers = ["ID", "Name", "Status", "Image", "Action", "Delete"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                self.scroll_frame,
                text=header,
                text_color="#cccccc",
                font=ctk.CTkFont(size=12, weight="bold"),
            ).grid(row=0, column=i, padx=10, pady=8, sticky="w")

    def load_containers(self):
        containers = self.controller.getAllContainers()

        for i, cont in enumerate(containers):
            row = i + 1
            padding = {"padx": 10, "pady": 5}

            ctk.CTkLabel(self.scroll_frame, text=cont["ID"], text_color="white").grid(
                row=row, column=0, **padding, sticky="w"
            )
            ctk.CTkLabel(self.scroll_frame, text=cont["Name"], text_color="white").grid(
                row=row, column=1, **padding, sticky="w"
            )
            ctk.CTkLabel(
                self.scroll_frame, text=cont["Status"], text_color="white"
            ).grid(row=row, column=2, **padding, sticky="w")
            ctk.CTkLabel(
                self.scroll_frame, text=cont["Image"], text_color="white"
            ).grid(row=row, column=3, **padding, sticky="w")

            # Action Button
            action_text = "Stop" if cont["Running"] else "Run"
            is_running = cont["Running"]

            btn_color = "#8a1f1f" if is_running else "#1f8a53"
            hover_color = "#c0392b" if is_running else "#27ae60"

            ctk.CTkButton(
                self.scroll_frame,
                text=action_text,
                width=80,
                fg_color=btn_color,
                hover_color=hover_color,
                text_color="white",
                command=lambda c_id=cont["ID"], running=is_running: (
                    self.stop_container(c_id) if running else self.run_container(c_id)
                ),
            ).grid(row=row, column=4, padx=10, pady=5)

            ctk.CTkButton(
                self.scroll_frame,
                text="Delete",
                width=80,
                fg_color="#8a1f1f",
                hover_color="#c0392b",
                text_color="white",
                command=lambda c_id=cont["ID"]: self.delete_container(c_id),
            ).grid(row=row, column=5, padx=10, pady=5)

    def delete_container(self, container_id):
        confirm = messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this container?"
        )
        if not confirm:
            return

        self.show_progress_bar()

        def action():
            res, msg = self.controller.deleteContainer(container_id)
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
            self.refresh()

        threading.Thread(target=action, daemon=True).start()
        threading.Thread(target=self.progress_loop, daemon=True).start()

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
            self.refresh()

        threading.Thread(target=action, daemon=True).start()
        threading.Thread(target=self.progress_loop, daemon=True).start()

    def show_progress_bar(self):
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(0, 10))

    def progress_loop(self):
        progress = 0.0
        while threading.active_count() > 2 and progress < 0.95:
            progress += 0.01
            try:
                self.window.after(0, lambda p=progress: self.progress_bar.set(p))
                time.sleep(0.05)
            except:
                break

    def refresh(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.create_headers()
        self.load_containers()

    def go_back(self):
        self.window.destroy()
        from view.createDockerFile import CreateDockerfilePage

        CreateDockerfilePage(self.root)

    def on_close(self):
        self.window.destroy()
        self.root.deiconify()
