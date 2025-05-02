import tkinter as tk
from tkinter import ttk, filedialog
import webbrowser
from controller import Controller


# ---------------- Virtual Disk Page Class ---------------- #
class CreateVirtualDiskPage:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Create Virtual Disk")
        self.window.geometry("800x500")

        # Sidebar
        self.sidebar = tk.Frame(self.window, width=150, bg="#0c28b3")
        self.sidebar.pack(side="left", fill="y")

        tk.Button(
            self.sidebar,
            text="Home",
            fg="#0c28b3",
            font=("Arial", 12),
            relief="flat",
            command=self.go_home,
        ).pack(pady=10, fill="x")
        tk.Button(
            self.sidebar,
            text="Create Disk",
            fg="#0c28b3",
            font=("Arial", 12, "bold"),
            relief="flat",
            state="disabled",
        ).pack(pady=10, fill="x")
        tk.Button(
            self.sidebar,
            text="Create VM",
            fg="#0c28b3",
            font=("Arial", 12),
            relief="flat",
            command=self.go_vm,
        ).pack(pady=10, fill="x")

        # Main area
        self.main_frame = tk.Frame(self.window, bg="white", padx=40)
        self.main_frame.pack(side="right", fill="both", expand=True, anchor="nw")

        tk.Label(
            self.main_frame,
            text="Create Virtual Disk",
            font=("Arial", 18),
            fg="#0c28b3",
            bg="white",
        ).pack(anchor="w", pady=(20, 10))

        # Disk Path
        tk.Label(self.main_frame, text="Disk Path:", bg="white").pack(anchor="w")
        path_frame = tk.Frame(self.main_frame, bg="white")
        path_frame.pack(anchor="w", fill="x", pady=5)
        self.disk_path = tk.Entry(path_frame, width=50)
        self.disk_path.pack(side="left")
        tk.Button(
            path_frame, text="Browse", command=self.browse_path, relief="flat"
        ).pack(side="left")

        # Disk Format
        tk.Label(self.main_frame, text="Disk Format:", bg="white").pack(
            anchor="w", pady=(10, 0)
        )
        self.disk_format = ttk.Combobox(
            self.main_frame, values=["qcow2", "vmdk", "vdi", "raw"]
        )
        self.disk_format.pack(anchor="w", pady=5)

        # Disk Size
        tk.Label(self.main_frame, text="Disk Size (GB):", bg="white").pack(
            anchor="w", pady=(10, 0)
        )
        self.disk_size = tk.Spinbox(self.main_frame, from_=1, to=1024)
        self.disk_size.pack(anchor="w", pady=5)

        # Buttons
        button_frame = tk.Frame(self.main_frame, bg="white")
        button_frame.pack(anchor="w", pady=20)
        tk.Button(button_frame, text="Back", command=self.back, relief="flat").pack(
            side="left"
        )
        tk.Button(
            button_frame, text="Create Disk", command=self.create_disk, relief="flat"
        ).pack(side="left")

        self.window.mainloop()

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.disk_path.delete(0, tk.END)
            self.disk_path.insert(0, path)

    def create_disk(self):
        print("Creating virtual disk...")
        print("Path:", self.disk_path.get())
        print("Format:", self.disk_format.get())
        print("Size:", self.disk_size.get(), "GB")

        controller = Controller()
        result = controller.callVD(
            "mazen",
            self.disk_path.get(),
            self.disk_format.get(),
            self.disk_size.get(),
        )
        print(result)

    def back(self):
        self.window.destroy()
        HomePage()

    def go_home(self):
        self.window.destroy()
        HomePage()

    def go_vm(self):
        self.window.destroy()
        CreateVirtualMachinePage()


# ---------------- Virtual Machine Page Class ---------------- #
class CreateVirtualMachinePage:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Create Virtual Machine")
        self.window.geometry("800x500")

        # Sidebar
        self.sidebar = tk.Frame(self.window, width=150, bg="#0c28b3")
        self.sidebar.pack(side="left", fill="y")

        tk.Button(
            self.sidebar,
            text="Home",
            fg="#0c28b3",
            font=("Arial", 12),
            relief="flat",
            command=self.go_home,
        ).pack(pady=10, fill="x")
        tk.Button(
            self.sidebar,
            text="Create Disk",
            fg="#0c28b3",
            font=("Arial", 12),
            relief="flat",
            command=self.go_vdisk,
        ).pack(pady=10, fill="x")
        tk.Button(
            self.sidebar,
            text="Create VM",
            fg="#0c28b3",
            font=("Arial", 12, "bold"),
            relief="flat",
            state="disabled",
        ).pack(pady=10, fill="x")

        # Main area
        self.main_frame = tk.Frame(self.window, bg="white", padx=40)
        self.main_frame.pack(side="right", fill="both", expand=True, anchor="nw")

        tk.Label(
            self.main_frame,
            text="Create Virtual Machine",
            font=("Arial", 18),
            fg="#0c28b3",
            bg="white",
        ).pack(anchor="w", pady=(20, 10))

        # Disk Path
        tk.Label(self.main_frame, text="Disk Path:", bg="white").pack(anchor="w")
        disk_frame = tk.Frame(self.main_frame, bg="white")
        disk_frame.pack(anchor="w", fill="x", pady=5)
        self.disk_path = tk.Entry(disk_frame, width=50)
        self.disk_path.pack(side="left")
        tk.Button(
            disk_frame, text="Browse", command=self.browse_disk_path, relief="flat"
        ).pack(side="left")

        # Memory (GB)
        tk.Label(self.main_frame, text="Memory (GB):", bg="white").pack(
            anchor="w", pady=(10, 0)
        )
        self.memory = tk.Spinbox(self.main_frame, from_=0, to=999999999999999)
        self.memory.pack(anchor="w", pady=5)

        # CPUs
        tk.Label(self.main_frame, text="CPUs:", bg="white").pack(
            anchor="w", pady=(10, 0)
        )
        self.cpus = tk.Spinbox(self.main_frame, from_=1, to=16)
        self.cpus.pack(anchor="w", pady=5)

        # ISO Path
        tk.Label(self.main_frame, text="ISO Path:", bg="white").pack(
            anchor="w", pady=(10, 0)
        )
        iso_frame = tk.Frame(self.main_frame, bg="white")
        iso_frame.pack(anchor="w", fill="x", pady=5)
        self.iso_path = tk.Entry(iso_frame, width=50)
        self.iso_path.pack(side="left")
        tk.Button(
            iso_frame, text="Browse", command=self.browse_iso_path, relief="flat"
        ).pack(side="left")

        # Buttons
        button_frame = tk.Frame(self.main_frame, bg="white")
        button_frame.pack(anchor="w", pady=20)
        tk.Button(button_frame, text="Back", command=self.back, relief="flat").pack(
            side="left"
        )
        tk.Button(
            button_frame, text="Create VM", command=self.create_vm, relief="flat"
        ).pack(side="left")

        self.window.mainloop()

    def browse_disk_path(self):
        path = filedialog.askopenfilename(title="Select Virtual Disk File")
        if path:
            self.disk_path.delete(0, tk.END)
            self.disk_path.insert(0, path)

    def browse_iso_path(self):
        path = filedialog.askopenfilename(title="Select ISO File")
        if path:
            self.iso_path.delete(0, tk.END)
            self.iso_path.insert(0, path)

    def create_vm(self):
        print("Creating virtual machine...")
        print("Disk Path:", self.disk_path.get())
        print("Memory:", self.memory.get(), "GB")
        print("CPUs:", self.cpus.get())
        print("ISO Path:", self.iso_path.get())

        controller = Controller()
        result = controller.callVM(
            self.disk_path.get(),
            self.memory.get(),
            self.cpus.get(),
            self.iso_path.get(),
        )
        print(result)

    def back(self):
        self.window.destroy()
        HomePage()

    def go_home(self):
        self.window.destroy()
        HomePage()

    def go_vdisk(self):
        self.window.destroy()
        CreateVirtualDiskPage()


# ---------------- Home Page ---------------- #
orders_data = [
    (
        "Virtual Disk",
        "A Virtual Disk is a file or set of files on a physical storage device that emulates a physical disk drive. It is used by virtual machines to store data, operating systems, and applications, functioning like a real hard drive within the virtual environment.",
        "https://www.youtube.com/watch?v=tTBt7_aACPI&t=14s",
    ),
    (
        "Virtual Machine",
        "A Virtual Machine (VM) is a software-based emulation of a physical computer that runs an operating system and applications in a completely isolated environment. It enables multiple OS instances to operate on a single physical machine, providing flexibility, scalability, and efficient resource utilization.",
        "https://www.youtube.com/watch?v=mQP0wqNT_DI",
    ),
]


def open_demo(url):
    webbrowser.open(url)


def open_vm_window(name, home_root):
    home_root.destroy()
    if name.lower() == "virtual disk":
        CreateVirtualDiskPage()
    elif name.lower() == "virtual machine":
        CreateVirtualMachinePage()


def HomePage():
    root = tk.Tk()
    root.title("Virtual Machines")
    root.geometry("1000x600")

    header_frame = tk.Frame(root, bg="#0c28b3")
    header_frame.pack(fill=tk.X)

    tk.Label(
        header_frame,
        text="Virtual Machines",
        font=("Arial", 24),
        bg="#0c28b3",
        fg="white",
    ).pack(side=tk.LEFT, padx=20)
    tk.Button(
        header_frame,
        text="+ VM",
        fg="#0c28b3",
        bg="#0c28b3",
        font=("Arial", 12),
        relief="flat",
        command=lambda: open_vm_window("virtual machine", root),
    ).pack(side=tk.RIGHT, padx=20)
    tk.Button(
        header_frame,
        text="+ VDisk",
        fg="#0c28b3",
        font=("Arial", 12),
        relief="flat",
        command=lambda: open_vm_window("virtual disk", root),
    ).pack(side=tk.RIGHT, padx=10)

    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tk.Label(
        scrollable_frame,
        text="Type",
        font=("Arial", 10, "bold"),
        width=20,
        anchor="w",
        bg="#e6e6e6",
    ).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    tk.Label(
        scrollable_frame,
        text="Description",
        font=("Arial", 10, "bold"),
        width=60,
        anchor="w",
        bg="#e6e6e6",
    ).grid(row=0, column=1, padx=10, pady=5, sticky="w")
    tk.Label(
        scrollable_frame,
        text="Demo",
        font=("Arial", 10, "bold"),
        width=10,
        anchor="center",
        bg="#e6e6e6",
    ).grid(row=0, column=2, padx=10, pady=5)
    tk.Label(
        scrollable_frame,
        text="Start",
        font=("Arial", 10, "bold"),
        width=10,
        anchor="center",
        bg="#e6e6e6",
    ).grid(row=0, column=3, padx=10, pady=5)

    for i, order in enumerate(orders_data, start=1):
        tk.Label(scrollable_frame, text=order[0], width=20, anchor="w").grid(
            row=i, column=0, padx=10, pady=5, sticky="w"
        )
        tk.Label(
            scrollable_frame,
            text=order[1],
            width=60,
            anchor="w",
            justify="left",
            wraplength=500,
        ).grid(row=i, column=1, padx=10, pady=5, sticky="w")
        tk.Button(
            scrollable_frame,
            text="Watch",
            command=lambda url=order[2]: open_demo(url),
            relief="flat",
        ).grid(row=i, column=2, padx=10, pady=5)

        start_label = "Start VD" if order[0].lower() == "virtual disk" else "Start VM"
        tk.Button(
            scrollable_frame,
            text=start_label,
            command=lambda name=order[0]: open_vm_window(name, root),
            relief="flat",
        ).grid(row=i, column=3, padx=10, pady=5)

    root.mainloop()


# Run the home page
HomePage()
