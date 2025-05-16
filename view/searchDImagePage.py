import customtkinter as ctk
from tkinter import messagebox
from controller.controllerDocker import DockerController


class SearchDockerImagePage:
    def __init__(self, root):
        self.root = root
        self.controller = DockerController()
        self.window = ctk.CTkToplevel(fg_color="#545454")
        self.window.title("Search Docker Image")
        self.window.geometry("900x500")

        ctk.CTkLabel(
            self.window,
            text="🔍 Search for a Docker Image",
            font=("Segoe UI", 20, "bold"),
            text_color="white"
        ).pack(pady=20)

        self.search_entry = ctk.CTkEntry(
            self.window,
            placeholder_text="Enter image name (e.g., nginx)",
            width=400
        )
        self.search_entry.pack(pady=10)

        ctk.CTkButton(
            self.window,
            text="Search",
            command=self.perform_search,
            fg_color="#007bff",
            text_color="white",
            width=150
        ).pack(pady=10)

        self.result_frame = ctk.CTkFrame(self.window, fg_color="#3a3a3a")
        self.result_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkButton(
            self.window,
            text="Back",
            command=self.go_back,
            fg_color="#444",
            hover_color="#222",
            text_color="white",
            width=100
        ).pack(anchor="w", padx=20, pady=10)

    def perform_search(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter an image name.")
            return

        res, images = self.controller.searchImage(query)

        if not res:
            messagebox.showerror("Error", "Something went wrong while searching.")
            return

        if len(images) == 0:
            ctk.CTkLabel(self.result_frame, text="No images found.", text_color="white").pack(pady=10)
            return

        # Only show the first matched result
        img = images[0]  # Take the first match

        ctk.CTkLabel(
            self.result_frame,
            text=f"🖼 Repository: {img['Repository']}",
            text_color="white",
            font=("Segoe UI", 16)
        ).pack(anchor="w", pady=5)
        ctk.CTkLabel(
            self.result_frame,
            text=f"🔖 Tag: {img['Tag']}",
            text_color="white"
        ).pack(anchor="w", pady=5)
        ctk.CTkLabel(
            self.result_frame,
            text=f"🆔 Image ID: {img['ImageID']}",
            text_color="white"
        ).pack(anchor="w", pady=5)
        ctk.CTkLabel(
            self.result_frame,
            text=f"📅 Created: {img['Created']}",
            text_color="white"
        ).pack(anchor="w", pady=5)
        ctk.CTkLabel(
            self.result_frame,
            text=f"📦 Size: {img['Size']}",
            text_color="white"
        ).pack(anchor="w", pady=5)

        # Buttons Frame
        btn_frame = ctk.CTkFrame(self.result_frame, fg_color="#3a3a3a")
        btn_frame.pack(pady=20)

        full_name = f"{img['Repository']}:{img['Tag']}"

        # Run Button
        ctk.CTkButton(
            btn_frame,
            text="Run",
            fg_color="#28a745",
            text_color="white",
            width=100,
            command=lambda: self.run_image(img['Repository'], img['Tag'])
        ).pack(side="left", padx=10)

        # Delete Button
        ctk.CTkButton(
            btn_frame,
            text="Delete",
            fg_color="red",
            text_color="white",
            width=100,
            command=lambda: self.delete_image(img["ImageID"])
        ).pack(side="left", padx=10)

    def run_image(self, name, tag):
        from view.runImagePage import RunDockerImagePage
        self.window.after(100, self.window.destroy)
        RunDockerImagePage(self.root, {"Image": name, "Tag": tag})


    def delete_image(self, full_name):
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {full_name}?")
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
        self.window.after(100, self.window.destroy)
        self.root.deiconify()
