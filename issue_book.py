import customtkinter as ctk
from tkinter import messagebox
from database import conn, cursor
from theme import TITLE_FONT, LABEL_FONT
from datetime import date

def open_window():
    win = ctk.CTk()
    win.title("Asset Issuance Protocol")
    win.geometry("450x420")
    win.resizable(False, False)

    ctk.CTkLabel(win, text="Issue Book Asset", font=TITLE_FONT).pack(pady=(40, 25))

    fields = [("Student ID", "sid"), ("Book ID", "bid"), ("Issue Date", "idate")]
    entries = {}

    form_frame = ctk.CTkFrame(win, fg_color="transparent")
    form_frame.pack(pady=5)

    for label_text, key in fields:
        f = ctk.CTkFrame(form_frame, fg_color="transparent", width=320, height=45)
        f.pack(fill="x", pady=8)
        f.pack_propagate(False)
        
        ctk.CTkLabel(f, text=label_text, font=LABEL_FONT, width=100, anchor="w").pack(side="left")
        entry = ctk.CTkEntry(f, corner_radius=8)
        entry.pack(side="right", fill="x", expand=True)
        if key == "idate":
            entry.insert(0, str(date.today()))
        entries[key] = entry

    def process_issuance():
        s = entries['sid'].get()
        b = entries['bid'].get()
        d = entries['idate'].get()

        if not all([s, b, d]):
            messagebox.showerror("Validation Error", "All fields require runtime signatures.")
            return

        cursor.execute("SELECT * FROM Student WHERE student_id=%s", (s,))
        if not cursor.fetchone():
            messagebox.showerror("System Match Missing", "Target Student tracking identity missing.")
            return

        cursor.execute("SELECT * FROM Book WHERE book_id=%s", (b,))
        book = cursor.fetchone()
        if not book:
            messagebox.showerror("System Match Missing", "Target Inventory profile object missing.")
            return

        if book[5] <= 0:
            messagebox.showwarning("Unavailable", "No physically redundant units remain on deck.")
            return

        cursor.execute("INSERT INTO Issue_Book (student_id, book_id, issue_date) VALUES(%s,%s,%s)", (s, b, d))
        cursor.execute("UPDATE Book SET available=available-1 WHERE book_id=%s", (b,))
        conn.commit()
        
        messagebox.showinfo("Voucher Success", "Asset lease balance synchronized.")
        win.destroy()

    ctk.CTkButton(win, text="Authorize Issue", width=320, height=42, corner_radius=8, font=("Segoe UI", 13, "bold"), command=process_issuance).pack(pady=(25, 0))
    win.mainloop()