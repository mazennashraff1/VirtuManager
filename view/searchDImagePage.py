import customtkinter as ctk
from tkinter import messagebox
from controller.controllerDocker import DockerController


class SearchDockerImagePage:
    def __init__(self, root):
        self.root = root
        self.controller = DockerController()
        self.window = ctk.CTkToplevel(fg_color="#1e1e1e")
        self.window.title("Search Docker Image")
        self.window.geometry("880x540")

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
            height=35,
        ).pack(anchor="nw", pady=15, padx=20)

        # --- Main Section ---
        self.main_frame = ctk.CTkFrame(self.window, fg_color="#1e1e1e")
        self.main_frame.pack(fill="both", expand=True, padx=50, pady=10)

        ctk.CTkLabel(
            self.main_frame,
            text="🔍 Search for a Docker Image",
            font=("Segoe UI", 22, "bold"),
            text_color="white",
        ).pack(anchor="w", pady=(0, 15))

        self.search_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter image name (e.g., nginx)",
            width=460,
        )
        self.search_entry.pack(anchor="w", pady=5)

        ctk.CTkButton(
            self.main_frame,
            text="Search",
            command=self.perform_search,
            fg_color="#007bff",
            hover_color="#0056b3",
            text_color="white",
            width=140,
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w", pady=12)

        self.result_frame = ctk.CTkFrame(
            self.main_frame, fg_color="#2e2e2e", corner_radius=8
        )
        self.result_frame.pack(fill="both", expand=True, pady=20)

    def perform_search(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter an image name.")
            return

        res, images = self.controller.searchImage(query)

        if not res:
            messagebox.showerror("Error", images)
            return

        if len(images) == 0:
            ctk.CTkLabel(
                self.result_frame,
                text="⚠️ No images found.",
                text_color="white",
                font=ctk.CTkFont(size=14),
            ).pack(pady=10)
            return

        img = images[0]  # First match only

        ctk.CTkLabel(
            self.result_frame,
            text=f"🖼 Repository: {img['Repository']}",
            text_color="white",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w", pady=8, padx=20)

        for label, icon in [
            (f"🔖 Tag: {img['Tag']}", 5),
            (f"🆔 Image ID: {img['ImageID']}", 5),
            (f"📅 Created: {img['Created']}", 5),
            (f"📦 Size: {img['Size']}", 10),
        ]:
            ctk.CTkLabel(
                self.result_frame, text=label, text_color="white", font=("Segoe UI", 13)
            ).pack(anchor="w", pady=(icon, 0), padx=20)

        # Buttons
        btn_frame = ctk.CTkFrame(self.result_frame, fg_color="#2e2e2e")
        btn_frame.pack(pady=25)

        full_name = f"{img['Repository']}:{img['Tag']}"

        ctk.CTkButton(
            btn_frame,
            text="▶ Run",
            fg_color="#28a745",
            hover_color="#218838",
            text_color="white",
            width=120,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: self.run_image(img["Repository"], img["Tag"]),
        ).pack(side="left", padx=15)

        ctk.CTkButton(
            btn_frame,
            text="🗑 Delete",
            fg_color="#dc3545",
            hover_color="#b02a37",
            text_color="white",
            width=120,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: self.delete_image(img["ImageID"]),
        ).pack(side="left", padx=15)

    def run_image(self, name, tag):
        from view.runImagePage import RunDockerImagePage

        self.window.after(100, self.window.destroy)
        RunDockerImagePage(self.root, {"Image": name, "Tag": tag})

    def delete_image(self, full_name):
        confirm = messagebox.askyesno(
            "Confirm Deletion", f"Are you sure you want to delete {full_name}?"
        )
        if not confirm:
            return

        success, message = self.controller.deleteImage(full_name)
        if success:
            messagebox.showinfo("Deleted", message)
            for widget in self.result_frame.winfo_children():
                widget.destroy()
        else:
            messagebox.showerror("Error", message)

    def go_back(self):
        self.window.destroy()
        from view.createDockerFile import CreateDockerfilePage

        CreateDockerfilePage(self.root)
