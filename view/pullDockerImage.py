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


class DockerImagePullPage:
    def __init__(self, root):
        self.controller = DockerController()
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#545454")
        self.window.title("Docker Image Pull")
        self.window.geometry("800x500")

        self.sidebar = ctk.CTkFrame(self.window, width=160, fg_color="white")
        self.sidebar.pack(side="left", fill="y")
        add_sidebar_button(self.sidebar, "Home", self.go_home)
        add_sidebar_button(self.sidebar, "Pull Image", None, disabled=True)

        self.main_frame = ctk.CTkFrame(self.window, fg_color="#545454")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(
            self.main_frame,
            text="Search & Pull Docker Image",
            font=("Segoe UI", 20, "bold"),
            text_color="white",
        ).pack(anchor="w", pady=(0, 20))

        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(
            self.main_frame, textvariable=self.search_var, width=400
        )
        self.search_entry.pack(anchor="w", pady=6)
        self.search_entry.bind("<KeyRelease>", self.search_images)

        self.suggestions_list = tk.Listbox(self.main_frame, height=8, width=60)
        self.suggestions_list.pack(anchor="w")
        self.suggestions_list.bind("<<ListboxSelect>>", self.show_image_details)

        self.description_text = ctk.CTkTextbox(
            self.main_frame,
            width=600,
            height=150,
            wrap="word",
            font=("Segoe UI", 12),
            text_color="white",
            fg_color="#3a3a3a",
            scrollbar_button_color="#5a5a5a",
        )
        self.description_text.pack(anchor="w", pady=10)
        self.description_text.configure(state="disabled")  # Make it read-only
        self.pull_button = ctk.CTkButton(
            self.main_frame,
            text="Pull Selected Image",
            command=self.pull_image,
            fg_color="#004aad",
            hover_color="#003180",
            text_color="white",
            width=200,
        )
        self.pull_button.pack(pady=10)

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

        if not results:
            print("No results found.")
        else:
            for image in results:
                repo_name = image.get("repo_name")
                if not repo_name:
                    continue
                full_name = repo_name
                self.image_data_map[full_name] = image
                self.suggestions_list.insert(tk.END, full_name)

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
            if selected:
                res, msg = self.controller.pullDockerImage(selected)
                if res:
                    messagebox.showinfo("Success", msg)
                else:
                    messagebox.showerror("Error", msg)
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")

    def go_home(self):
        self.window.destroy()
        self.root.deiconify()
