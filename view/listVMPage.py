import customtkinter as ctk


class ListVirtualMachinesPage:
    def __init__(self, root):
        self.root = root
        self.window = ctk.CTkToplevel(fg_color="#545454")
        self.window.title("List Virtual Machines")
        self.window.geometry("800x500")

        ctk.CTkLabel(
            self.window,
            text="All Virtual Machines",
            font=("Segoe UI", 18, "bold"),
            text_color="white",
        ).pack(pady=20)

        # Scrollable frame for table content
        scroll_frame = ctk.CTkScrollableFrame(self.window, fg_color="#545454")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Table headers
        headers = ["VM Name", "Disk", "Memory", "CPU", "Action"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                scroll_frame,
                text=header,
                font=("Segoe UI", 14, "bold"),
                text_color="white",
                width=120,
            ).grid(row=0, column=col, padx=5, pady=5)

        # Load data from file
        try:
            with open("logs/allVM.txt", "r") as file:
                lines = file.readlines()

            for i, line in enumerate(lines, start=1):
                parts = line.strip().split(",")
                if len(parts) != 4:
                    continue  # skip malformed lines

                vm_name, disk, memory, cpu = parts

                ctk.CTkLabel(
                    scroll_frame, text=vm_name, text_color="white", width=120
                ).grid(row=i, column=0, padx=5, pady=5)
                ctk.CTkLabel(
                    scroll_frame, text=disk, text_color="white", width=120
                ).grid(row=i, column=1, padx=5, pady=5)
                ctk.CTkLabel(
                    scroll_frame, text=memory, text_color="white", width=120
                ).grid(row=i, column=2, padx=5, pady=5)
                ctk.CTkLabel(
                    scroll_frame, text=cpu, text_color="white", width=120
                ).grid(row=i, column=3, padx=5, pady=5)

                # Start Button
                ctk.CTkButton(
                    scroll_frame,
                    text="Start",
                    command=lambda name=vm_name: self.start_vm(name),
                    fg_color="#228B22",  # Green
                    text_color="white",
                    width=80,
                ).grid(row=i, column=4, padx=5, pady=5)

        except FileNotFoundError:
            ctk.CTkLabel(
                self.window, text="Error: allVM.txt not found", text_color="red"
            ).pack(pady=10)

    def start_vm(self, vm_name):
        # Here you would call your controller or system command to start the VM
        print(f"Starting VM: {vm_name}")
