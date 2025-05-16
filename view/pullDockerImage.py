import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from controller.controllerDocker import DockerController
import threading
import time


class DockerImagePullPage:
    def __init__(self, root):
        self.controller = DockerController()
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#1e1e1e")
        self.window.title("Docker Image Pull")
        self.window.geometry("850x640")

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
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=10)

        ctk.CTkLabel(
            self.main_frame,
            text="🔍 Search & Pull Docker Image",
            font=("Segoe UI", 22, "bold"),
            text_color="white",
        ).pack(anchor="w", pady=(0, 20))

        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(
            self.main_frame,
            textvariable=self.search_var,
            width=500
        )
        self.search_entry.pack(anchor="w", pady=6)
        self.search_entry.bind("<KeyRelease>", self.search_images)

        self.suggestions_list = tk.Listbox(
            self.main_frame,
            height=8,
            width=75,
            bg="#1e1e1e",                # darker background
            fg="white",                  # white text
            font=("Segoe UI", 11),
            selectbackground="#5c1e1e",  # red hover-like selection
            selectforeground="white",
            highlightthickness=2,
            highlightbackground="#444",  # border color
            relief="flat",
            bd=0,
            activestyle="dotbox"         # optional: visual cue for active row
        )

        self.suggestions_list.pack(anchor="w", pady=(6, 10))
        self.suggestions_list.bind("<<ListboxSelect>>", self.show_image_details)

        ctk.CTkLabel(
            self.main_frame,
            text="📝 Image Info",
            text_color="white",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(10, 5))

        self.description_text = ctk.CTkTextbox(
            self.main_frame,
            width=700,
            height=160,
            wrap="word",
            font=("Courier New", 12),
            text_color="white",
            fg_color="#2c2c2c",
            border_color="#444",
            border_width=2
        )
        self.description_text.pack(anchor="w", pady=8)
        self.description_text.configure(state="disabled")

        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(anchor="center", pady=(5, 20))

        self.pull_button = ctk.CTkButton(
            self.button_frame,
            text="⬇️ Pull Selected Image",
            command=self.pull_image,
            fg_color="#004aad",
            hover_color="#003180",
            text_color="white",
            width=220,
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8
        )
        self.pull_button.pack()


        # Progress bar setup (initially hidden)
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=500)
        self.progress_bar.set(0)

        self.image_data_map = {}

    def search_images(self, event):
        query = self.search_var.get().strip()
        if len(query) < 2:
            self.suggestions_list.delete(0, tk.END)
            return

        try:
            results = self.controller.fetchDockerImages(query)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.suggestions_list.delete(0, tk.END)
        self.image_data_map = {}

        for image in results:
            repo_name = image.get("repo_name")
            if repo_name:
                self.image_data_map[repo_name] = image
                self.suggestions_list.insert(tk.END, repo_name)

    def show_image_details(self, event):
        try:
            selection = self.suggestions_list.curselection()
            if not selection:
                return
            selected = self.suggestions_list.get(selection[0])
            image_info = self.image_data_map.get(selected, {})

            desc = image_info.get("short_description", "No description available.")
            stars = image_info.get("star_count", 0)
            pulls = image_info.get("pull_count", 0)
            is_automated = image_info.get("is_automated", False)
            is_official = image_info.get("is_official", False)

            details = (
                f"📦 Repository:\n  {selected}\n\n"
                f"⭐ Stars: {stars}\n"
                f"⬇️ Pulls: {pulls:,}\n"
                f"🤖 Automated: {'Yes' if is_automated else 'No'}\n"
                f"🏆 Official: {'Yes' if is_official else 'No'}\n\n"
                f"📝 Description:\n  {desc}"
            )

            self.description_text.configure(state="normal")
            self.description_text.delete("1.0", tk.END)
            self.description_text.insert("1.0", details)
            self.description_text.configure(state="disabled")

        except Exception as e:
            print("Error displaying image details:", e)

    def pull_image(self):
        try:
            selection = self.suggestions_list.curselection()
            if not selection:
                return
            selected = self.suggestions_list.get(selection[0])
            if not selected:
                return

            self.progress_bar.pack(pady=(0, 10))
            self.progress_bar.set(0)

            def do_pull():
                progress = 0.0
                while progress < 0.95:
                    progress += 0.01
                    try:
                        self.window.after(0, lambda p=progress: self.progress_bar.set(p))
                        time.sleep(0.05)
                    except:
                        break

                res, msg = self.controller.pullDockerImage(selected)

                self.window.after(0, lambda: self.progress_bar.set(1.0))
                time.sleep(0.5)
                self.window.after(0, self.progress_bar.pack_forget)

                if res:
                    self.window.after(0, lambda: messagebox.showinfo("Success", msg))
                else:
                    self.window.after(0, lambda: messagebox.showerror("Error", msg))

            threading.Thread(target=do_pull, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")

    

    def go_back(self):
        self.window.destroy()
        from view.createDockerFile import CreateDockerfilePage
        CreateDockerfilePage(self.root)
