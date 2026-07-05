import customtkinter as ctk
from tkinter import messagebox
from database import conn, cursor
from theme import TITLE_FONT, LABEL_FONT

def open_window():
    win = ctk.CTk()
    win.title("Add New Catalog Item")
    win.geometry("450x480")
    win.resizable(False, False)

    ctk.CTkLabel(win, text="Add New Book", font=TITLE_FONT).pack(pady=(40, 25))

    fields = ["Title", "Author", "Category", "Quantity"]
    entries = {}

    # Unified container to keep input dimensions strictly aligned
    form_frame = ctk.CTkFrame(win, fg_color="transparent")
    form_frame.pack(pady=10)

    for field in fields:
        frame = ctk.CTkFrame(form_frame, fg_color="transparent", width=320, height=45)
        frame.pack(fill="x", pady=8)
        frame.pack_propagate(False)
        
        lbl = ctk.CTkLabel(frame, text=field, font=LABEL_FONT, width=90, anchor="w")
        lbl.pack(side="left")
        
        entry = ctk.CTkEntry(frame, placeholder_text=f"Enter {field}", corner_radius=8)
        entry.pack(side="right", fill="x", expand=True)
        entries[field.lower()] = entry

    def submit_data():
        t = entries['title'].get()
        a = entries['author'].get()
        c = entries['category'].get()
        q = entries['quantity'].get()

        if not all([t, a, c, q]):
            messagebox.showerror("Error", "All fields are mandatory.")
            return
        try:
            qty = int(q)
        except ValueError:
            messagebox.showerror("Error", "Quantity field must be an integer numeric value.")
            return

        query = "INSERT INTO Book(title, author, category, quantity, available) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(query, (t, a, c, qty, qty))
        conn.commit()
        messagebox.showinfo("Success", "Catalog entry recorded successfully.")
        win.destroy()

    ctk.CTkButton(win, text="Save Asset", width=320, height=42, corner_radius=8, font=("Segoe UI", 13, "bold"), command=submit_data).pack(pady=(25, 0))
    win.mainloop()