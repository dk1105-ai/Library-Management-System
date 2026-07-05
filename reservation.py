import customtkinter as ctk
from tkinter import messagebox
from database import conn, cursor
from theme import TITLE_FONT, LABEL_FONT
from datetime import date

def open_window():
    win = ctk.CTk()
    win.title("Hold / Reservation Queue")
    win.geometry("450x420")
    win.resizable(False, False)

    ctk.CTkLabel(win, text="Manage Reservations", font=TITLE_FONT).pack(pady=(40, 25))

    fields = [("Student ID", "sid"), ("Book ID", "bid"), ("Reserve Date", "resdate")]
    entries = {}

    form_frame = ctk.CTkFrame(win, fg_color="transparent")
    form_frame.pack(pady=5)

    for lbl, key in fields:
        f = ctk.CTkFrame(form_frame, fg_color="transparent", width=320, height=45)
        f.pack(fill="x", pady=8)
        f.pack_propagate(False)
        
        ctk.CTkLabel(f, text=lbl, font=LABEL_FONT, width=100, anchor="w").pack(side="left")
        entry = ctk.CTkEntry(f, corner_radius=8)
        entry.pack(side="right", fill="x", expand=True)
        if key == "resdate":
            entry.insert(0, str(date.today()))
        entries[key] = entry

    def commit_reservation():
        s, b, d = entries['sid'].get(), entries['bid'].get(), entries['resdate'].get()
        if not all([s, b, d]): return

        cursor.execute("SELECT * FROM Student WHERE student_id=%s", (s,))
        if not cursor.fetchone():
            messagebox.showerror("Error", "Student verification sequence failure.")
            return

        cursor.execute("SELECT available FROM Book WHERE book_id=%s", (b,))
        data = cursor.fetchone()
        if not data:
            messagebox.showerror("Error", "Book identifier indexing failed.")
            return

        if data[0] > 0:
            messagebox.showinfo("Active State Alert", "Stock volumes exist in inventory. Reservation request dropped.")
            return

        cursor.execute("INSERT INTO Reservation (student_id,book_id,reservation_date) VALUES(%s,%s,%s)", (s, b, d))
        conn.commit()
        messagebox.showinfo("Success", "Hold placement registered inside index queue.")
        win.destroy()

    ctk.CTkButton(win, text="Place Reservation Hold", width=320, height=42, corner_radius=8, font=("Segoe UI", 13, "bold"), command=commit_reservation).pack(pady=(25, 0))
    win.mainloop()