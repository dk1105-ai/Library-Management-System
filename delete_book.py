import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
from database import conn, cursor
from stack import deleted_books
from theme import TITLE_FONT, LABEL_FONT

def open_window():
    win = ctk.CTk()
    win.title("Remove Catalog Item")
    win.geometry("450x300")
    win.resizable(False, False)

    ctk.CTkLabel(win, text="Delete Book", font=TITLE_FONT).pack(pady=(40, 25))

    frame = ctk.CTkFrame(win, fg_color="transparent", width=320, height=45)
    frame.pack(pady=10)
    frame.pack_propagate(False)

    ctk.CTkLabel(frame, text="Book ID", font=LABEL_FONT, width=90, anchor="w").pack(side="left")
    id_entry = ctk.CTkEntry(frame, placeholder_text="Enter Book ID", corner_radius=8)
    id_entry.pack(side="right", fill="x", expand=True)

    def process_deletion():
        bid = id_entry.get()
        if not bid:
            messagebox.showerror("Error", "Please input an active Book ID.")
            return

        cursor.execute("SELECT * FROM Book WHERE book_id=%s", (bid,))
        res = cursor.fetchone()
        if not res:
            messagebox.showerror("Error", "No record matches this ID.")
            return

        try:
            deleted_books.append(res)
            cursor.execute("DELETE FROM Book WHERE book_id=%s", (bid,))
            conn.commit()
            messagebox.showinfo("Success", "Item cleanly dropped from registry.")
            win.destroy()
        except mysql.connector.Error as err:
            if err.errno == 1451:
                messagebox.showerror("Error", "Foreign key constraint failure: Active loans depend on this asset.")
            else:
                messagebox.showerror("Database Error", str(err))

    ctk.CTkButton(win, text="Delete Permanently", fg_color="#DC2626", hover_color="#991B1B", width=320, height=42, corner_radius=8, font=("Segoe UI", 13, "bold"), command=process_deletion).pack(pady=(20, 0))
    win.mainloop()