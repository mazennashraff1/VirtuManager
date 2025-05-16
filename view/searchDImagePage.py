import customtkinter as ctk
from controller.controllerDocker import DockerController


class SearchDockerImagePage:
    def __init__(self, root):
        self.root = root
        self.controller = DockerController()
        self.window = ctk.CTkToplevel(fg_color="#545454")
        self.window.title("Search Docker Image")
        self.window.geometry("800x500")

        ctk.CTkLabel(
            self.window,
            text="Search for a Docker Image",
            font=("Segoe UI", 20, "bold"),
            text_color="white",
        ).pack(pady=20)

        self.search_entry = ctk.CTkEntry(
            self.window, placeholder_text="Enter image name..."
        )
        self.search_entry.pack(pady=10)

        ctk.CTkButton(
            self.window,
            text="Search",
            command=self.perform_search,
            fg_color="#007bff",
            text_color="white",
        ).pack(pady=10)

        self.results_textbox = ctk.CTkTextbox(self.window, width=600, height=300)
        self.results_textbox.pack(pady=20)

    def perform_search(self):
        query = self.search_entry.get().strip()
        res, data = self.controller.searchImage(query)
        # Placeholder for search logic
        self.results_textbox.insert("1.0", f"{data}")
