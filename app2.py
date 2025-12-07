import tkinter as tk
from tkinter import ttk, messagebox, StringVar, IntVar

# ---------------- Config ----------------
MAX_PAGES = 8
MIN_FRAMES = 4
MAX_FRAMES = 6
MAX_ROWS = 100  

# ----------------- App -------------------
class PageTableApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Page Table Translator — Dark Theme")
        self.geometry("920x560")
        self.minsize(900, 520)
        self.configure(bg="#202226")

        # state
        self.page_size = IntVar(value=1024)   # default 1024
        self.frames_count = IntVar(value=4)   # default 4
        self.logical_addr = StringVar()
        self.page_entries = []  

        # UI build
        self._setup_styles()
        self._build_layout()
        self._populate_default_page_table()

    # ---------- Styling ----------
    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")  

        # Colors for dark  look
        self.colors = {
            "bg": "#1e1f22",
            "panel": "#17181a",
            "accent": "#2f8cff",
            "muted": "#9aa0a6",
            "text": "#e6eef6",
            "card": "#242629",
            "row_alt": "#232426"
        }

        # General widget style
        style.configure("TLabel", background=self.colors["bg"], foreground=self.colors["text"], font=("Segoe UI", 10))
        style.configure("TButton", background=self.colors["panel"], foreground=self.colors["text"], font=("Segoe UI", 10), padding=6)
        style.map("TButton",
                  background=[("active", self.colors["card"])])
        style.configure("TEntry", fieldbackground="#2a2b2d", foreground=self.colors["text"])
        style.configure("TCombobox", fieldbackground="#2a2b2d", foreground=self.colors["text"])
        style.configure("TRadiobutton", background=self.colors["panel"], foreground=self.colors["text"])

        # Treeview style
        style.configure("Treeview",
                        background=self.colors["card"],
                        fieldbackground=self.colors["card"],
                        foreground=self.colors["text"],
                        rowheight=26,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        background=self.colors["panel"],
                        foreground=self.colors["text"],
                        font=("Segoe UI", 10, "bold"))

    # ---------- Layout ----------
    def _build_layout(self):
        # Main frames
        left_panel = tk.Frame(self, bg=self.colors["panel"], width=320, padx=12, pady=12)
        left_panel.pack(side="left", fill="y")
        right_panel = tk.Frame(self, bg=self.colors["bg"], padx=14, pady=12)
        right_panel.pack(side="right", expand=True, fill="both")

        # --- LEFT: control sidebar ---
        tk.Label(left_panel, text="Page Size", font=("Segoe UI", 11, "bold"), bg=self.colors["panel"], fg=self.colors["text"]).pack(anchor="w", pady=(2,6))

        rframe = tk.Frame(left_panel, bg=self.colors["panel"])
        rframe.pack(anchor="w", pady=(0,12))
        rb1 = ttk.Radiobutton(rframe, text="512", variable=self.page_size, value=512, command=self._on_pagesize_change)
        rb2 = ttk.Radiobutton(rframe, text="1024", variable=self.page_size, value=1024, command=self._on_pagesize_change)
        rb1.grid(row=0, column=0, padx=(0,8))
        rb2.grid(row=0, column=1, padx=(8,0))

        # Page table editor
        tk.Label(left_panel, text="Page Table Editor (use -1 for Not Loaded)", bg=self.colors["panel"], fg=self.colors["muted"]).pack(anchor="w", pady=(6,4))

        editor_frame = tk.Frame(left_panel, bg=self.colors["panel"])
        editor_frame.pack(fill="x", pady=(0,12))

        # header for editor
        tk.Label(editor_frame, text="Page", width=6, anchor="w", bg=self.colors["panel"], fg=self.colors["muted"]).grid(row=0, column=0, padx=(0,6))
        tk.Label(editor_frame, text="Frame", width=12, anchor="w", bg=self.colors["panel"], fg=self.colors["muted"]).grid(row=0, column=1, padx=(6,0))

        # create entries for page frames
        for i in range(MAX_PAGES):
            tk.Label(editor_frame, text=f"{i}", width=6, anchor="w", bg=self.colors["panel"], fg=self.colors["text"]).grid(row=i+1, column=0, pady=2)
            sv = StringVar()
            e = ttk.Entry(editor_frame, textvariable=sv, width=14)
            e.grid(row=i+1, column=1, pady=2, sticky="w")
            self.page_entries.append(sv)

        # frame count dropdown
        tk.Label(left_panel, text="Physical Frames (4 - 6)", bg=self.colors["panel"], fg=self.colors["muted"]).pack(anchor="w", pady=(8,4))
        self.cmb_frames = ttk.Combobox(left_panel, values=[4,5,6], state="readonly", textvariable=self.frames_count, width=8)
        self.cmb_frames.pack(anchor="w")
        self.cmb_frames.bind("<<ComboboxSelected>>", lambda e: self._on_frames_change())

        # logical address input
        tk.Label(left_panel, text="Logical Address (decimal)", bg=self.colors["panel"], fg=self.colors["muted"]).pack(anchor="w", pady=(12,4))
        ent_logical = ttk.Entry(left_panel, textvariable=self.logical_addr, width=20)
        ent_logical.pack(anchor="w")

        # buttons
        btn_frame = tk.Frame(left_panel, bg=self.colors["panel"])
        btn_frame.pack(anchor="w", pady=(14,8))
        btn_translate = ttk.Button(btn_frame, text="Translate", command=self.translate_address)
        btn_translate.grid(row=0, column=0, padx=(0,8))
        btn_clear = ttk.Button(btn_frame, text="Clear Table", command=self.clear_table)
        btn_clear.grid(row=0, column=1)

        # helpful note
        tk.Label(left_panel, text="Note: Use -1 for pages that are not loaded.\nFrames must be between 0 and selected frames-1.", bg=self.colors["panel"], fg=self.colors["muted"], justify="left", wraplength=290).pack(anchor="w", pady=(10,0))

        # --- RIGHT: output area ---
        top_label = tk.Label(right_panel, text="Translations Output", font=("Segoe UI", 12, "bold"), bg=self.colors["bg"], fg=self.colors["text"])
        top_label.pack(anchor="w")

        # treeview table inside a card
        table_card = tk.Frame(right_panel, bg=self.colors["card"], padx=8, pady=8)
        table_card.pack(fill="both", expand=True, pady=(8,8))

        cols = ("logical", "page", "frame", "offset", "physical", "fault")
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings", selectmode="browse", height=12)
        self.tree.heading("logical", text="Logical Addr")
        self.tree.heading("page", text="Page #")
        self.tree.heading("frame", text="Frame #")
        self.tree.heading("offset", text="Offset")
        self.tree.heading("physical", text="Physical Addr")
        self.tree.heading("fault", text="Page Fault")
        self.tree.column("logical", width=110, anchor="center")
        self.tree.column("page", width=70, anchor="center")
        self.tree.column("frame", width=70, anchor="center")
        self.tree.column("offset", width=80, anchor="center")
        self.tree.column("physical", width=140, anchor="center")
        self.tree.column("fault", width=100, anchor="center")

        vsb = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # bottom explanation box
        explanation_card = tk.Frame(right_panel, bg=self.colors["card"], padx=10, pady=8)
        explanation_card.pack(fill="x", pady=(6,0))
        tk.Label(explanation_card, text="Backend Explanation:", bg=self.colors["card"], fg=self.colors["muted"], anchor="w").pack(fill="x")
        self.explain = tk.Text(explanation_card, height=4, bg=self.colors["card"], fg=self.colors["text"], wrap="word", borderwidth=0)
        self.explain.pack(fill="x", pady=(6,0))
        self.explain.insert("1.0", "No translations yet. Explanation about what happened will appear here.")
        self.explain.configure(state="disabled")

    # ---------- Helpers ----------
    def _populate_default_page_table(self):
        # sample default mapping (values must be -1 or within frame range)
        defaults = ["0", "1", "-1", "3", "2", "-1", "-1", "-1"]
        for i, sv in enumerate(self.page_entries):
            sv.set(defaults[i] if i < len(defaults) else "-1")

    def _on_pagesize_change(self):
        # could show a tooltip or update explanation; keep it minimal
        self._write_explain(f"Page size set to {self.page_size.get()} bytes.")

    def _on_frames_change(self):
        val = self.frames_count.get()
        self._write_explain(f"Physical frames set to {val}. Valid frame numbers: 0 to {val-1}.")

    def _write_explain(self, text):
        self.explain.configure(state="normal")
        self.explain.delete("1.0", tk.END)
        self.explain.insert("1.0", text)
        self.explain.configure(state="disabled")

    def clear_table(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        self._write_explain("Table cleared. Page table remains unchanged.")

    # ---------- Core Logic ----------
    def translate_address(self):
        # Validate logical address
        try:
            logical = int(self.logical_addr.get().strip())
            if logical < 0:
                raise ValueError("Negative address")
        except Exception:
            messagebox.showerror("Invalid Input", "Enter a valid non-negative integer for Logical Address.")
            return

        # Validate page size
        ps = self.page_size.get()
        if ps not in (512, 1024):
            messagebox.showerror("Invalid Page Size", "Page size must be 512 or 1024.")
            return

        # Build page table from editor inputs
        page_table = []
        for i, sv in enumerate(self.page_entries):
            txt = sv.get().strip()
            if txt == "":
                # treat empty as -1 (not loaded)
                page_table.append(-1)
                continue
            try:
                v = int(txt)
            except Exception:
                messagebox.showerror("Invalid Page Table", f"Page {i} contains invalid integer.")
                return
            # allow -1 or valid frame
            if v != -1 and not (0 <= v <= self.frames_count.get() - 1):
                messagebox.showerror("Invalid Frame", f"Frame number for page {i} must be -1 or between 0 and {self.frames_count.get()-1}.")
                return
            page_table.append(v)

        # Calculate page number and offset carefully 
        page_number = logical // ps
        offset = logical % ps

        # If page_number outside allowed logical pages -> page fault / invalid
        if page_number >= len(page_table):
            fault_msg = f"Page number {page_number} is outside the logical address space (max {len(page_table)-1}). Treated as Page Fault."
            self._append_row(logical, page_number, "-", offset, "-", "YES")
            self._write_explain(fault_msg + "\n\nPage size: {} bytes. Page table length: {}. Frames available: {}."
                                .format(ps, len(page_table), self.frames_count.get()))
            return

        # Check mapping
        frame_number = page_table[page_number]

        if frame_number == -1:
            # Page fault occurred; not loaded
            self._append_row(logical, page_number, "N/A", offset, "N/A", "YES")
            explanation = (
                f"Page Fault: page {page_number} is not loaded (page table entry = -1).\n"
                f"Requested logical address {logical} → page {page_number}, offset {offset}.\n"
                f"No replacement/load simulated. To load the page, set a frame number (0..{self.frames_count.get()-1}) in the page table."
            )
            self._write_explain(explanation)
            return

        # Otherwise translate to physical address
        physical = frame_number * ps + offset
        self._append_row(logical, page_number, frame_number, offset, physical, "NO")
        explanation = (
            f"Translation successful:\nLogical addr {logical} → page {page_number}, offset {offset}.\n"
            f"Page {page_number} maps to frame {frame_number} → physical address = frame*pagesize + offset = {frame_number}*{ps} + {offset} = {physical}."
        )
        self._write_explain(explanation)

    def _append_row(self, logical, page, frame, offset, physical, fault):
        # enforce max rows
        rows = self.tree.get_children()
        if len(rows) >= MAX_ROWS:
            self.tree.delete(rows[0])

        self.tree.insert("", "end", values=(str(logical), str(page), str(frame), str(offset), str(physical), str(fault)))

# ----------------- Run -----------------
if __name__ == "__main__":
    app = PageTableApp()
    app.mainloop()