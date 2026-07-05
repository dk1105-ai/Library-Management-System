import customtkinter as ctk
from tkinter import messagebox
from database import conn, cursor
from theme import TITLE_FONT

def open_window():
    win = ctk.CTk()
    win.title("Catalog Lookup Engine")
    win.geometry("450x480")
    win.resizable(False, False)

    ctk.CTkLabel(win, text="Search Catalog", font=TITLE_FONT).pack(pady=(35, 15))

    search_frame = ctk.CTkFrame(win, fg_color="transparent", width=340, height=45)
    search_frame.pack(pady=10)
    search_frame.pack_propagate(False)

    search_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter Title or Book ID...", corner_radius=8)
    search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

    display_frame = ctk.CTkFrame(win, corner_radius=12, width=340)
    display_frame.pack(fill="both", expand=True, padx=40, pady=15)

    metrics = ["Book ID", "Title", "Author", "Category", "Quantity", "Available"]
    labels = {}

    for metric in metrics:
        f = ctk.CTkFrame(display_frame, fg_color="transparent")
        f.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(f, text=f"{metric}:", font=("Segoe UI", 12, "bold"), width=100, anchor="w").pack(side="left")
        val_lbl = ctk.CTkLabel(f, text="--", font=("Segoe UI", 12))
        val_lbl.pack(side="left", fill="x")
        labels[metric.lower().replace(" ", "_")] = val_lbl

    def execute_search():
        val = search_entry.get()
        if not val: return
        
        if val.isdigit():
            cursor.execute("SELECT * FROM Book WHERE book_id = %s", (val,))
        else:
            cursor.execute("SELECT * FROM Book WHERE title LIKE %s", (f"%{val}%",))
        
        res = cursor.fetchone()
        if res:
            for idx, key in enumerate(["book_id", "title", "author", "category", "quantity", "available"]):
                labels[key].configure(text=str(res[idx]))
        else:
            messagebox.showerror("Search Status", "No elements discovered in lookup space.")

    ctk.CTkButton(search_frame, text="Search", width=80, height=40, corner_radius=8, font=("Segoe UI", 12, "bold"), command=execute_search).pack(side="right")
    win.mainloop()