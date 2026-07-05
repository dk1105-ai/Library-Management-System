import customtkinter as ctk
from tkinter import messagebox
from database import conn, cursor
from datetime import datetime, date
from theme import TITLE_FONT, LABEL_FONT

def open_window():
    win = ctk.CTk()
    win.title("Asset Restitution Framework")
    win.geometry("450x420")
    win.resizable(False, False)

    ctk.CTkLabel(win, text="Return Book Asset", font=TITLE_FONT).pack(pady=(40, 25))

    fields = [("Student ID", "sid"), ("Book ID", "bid"), ("Return Date", "rdate")]
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
        if key == "rdate":
            entry.insert(0, str(date.today()))
        entries[key] = entry

    def process_return():
        s = entries['sid'].get()
        b = entries['bid'].get()
        r = entries['rdate'].get()

        if not all([s, b, r]):
            messagebox.showerror("Error", "Required fields empty.")
            return

        query = "SELECT issue_id, issue_date FROM Issue_Book WHERE student_id=%s AND book_id=%s AND return_date IS NULL"
        cursor.execute(query, (s, b))
        rec = cursor.fetchone()

        if not rec:
            messagebox.showerror("Zero State Error", "No record matching active transaction trace.")
            return

        iid, idate = rec[0], rec[1]
        try:
            r_obj = datetime.strptime(r, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Format mismatch", "Date string parser expects YYYY-MM-DD format.")
            return

        delta_days = (r_obj - idate).days
        fine = max(0, (delta_days - 7) * 10)

        cursor.execute("UPDATE Issue_Book SET return_date=%s, fine=%s WHERE issue_id=%s", (r, fine, iid))
        cursor.execute("UPDATE Book SET available = available + 1 WHERE book_id=%s", (b,))
        conn.commit()

        messagebox.showinfo("Processing Finalized", f"Asset checked in.\nOverdue assessments accrued: ₹{fine}")
        win.destroy()

    ctk.CTkButton(win, text="Process Return Receipt", width=320, height=42, corner_radius=8, font=("Segoe UI", 13, "bold"), command=process_return).pack(pady=(25, 0))
    win.mainloop()