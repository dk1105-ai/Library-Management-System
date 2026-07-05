import customtkinter as ctk
from tkinter import messagebox
from database import conn, cursor
from stack import deleted_books
from theme import TITLE_FONT

def open_window():
    win = ctk.CTk()
    win.title("Recovery System Engine")
    win.geometry("450x260")
    win.resizable(False, False)

    ctk.CTkLabel(win, text="Undo Delete Action", font=TITLE_FONT).pack(pady=(40, 20))

    def trigger_rollback():
        if not deleted_books:
            messagebox.showinfo("Rollback Engine Notice", "No deleted book history found.")
            return

        book = deleted_books.pop()
        query = "INSERT INTO Book (book_id, title, author, category, quantity, available) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, book)
        conn.commit()
        messagebox.showinfo("Success", "Last deleted book restored successfully!")
        win.destroy()

    # Clearer button wording as discussed
    ctk.CTkButton(win, text="Restore Last Deleted Book", fg_color="#10B981", hover_color="#047857", width=320, height=44, corner_radius=8, font=("Segoe UI", 13, "bold"), command=trigger_rollback).pack(pady=20)
    win.mainloop()