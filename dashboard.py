import customtkinter as ctk
from PIL import Image
import os

def start_dashboard():
    root = ctk.CTk()
    root.title("Smart Library Dashboard")
    root.geometry("500x650")
    root.resizable(False, False)

    # Clean window invocation functions
    def open_add_book(): import add_book; add_book.open_window()
    def open_delete_book(): import delete_book; delete_book.open_window()
    def open_search_book(): import search_book; search_book.open_window()
    def open_issue_book(): import issue_book; issue_book.open_window()
    def open_return_book(): import return_book; return_book.open_window()
    def open_reservation(): import reservation; reservation.open_window()
    def open_reports(): import reports; reports.open_window()
    def open_undo_delete(): import undo_delete; undo_delete.open_window()

    # App Logo using CTkImage natively
    img_path = "images/book.png"
    if os.path.exists(img_path):
        logo_img = ctk.CTkImage(light_image=Image.open(img_path), dark_image=Image.open(img_path), size=(70, 70))
        logo_label = ctk.CTkLabel(root, image=logo_img, text="")
        logo_label.pack(pady=(20, 5))

    ctk.CTkLabel(root, text="Library Management Dashboard", font=("Segoe UI", 22, "bold")).pack(pady=(5, 20))

    # Grid Container for uniform spacing layout
    btn_frame = ctk.CTkFrame(root, fg_color="transparent")
    btn_frame.pack(fill="both", expand=True, padx=40)

    buttons = [
        ("Add New Book", open_add_book),
        ("Delete Book", open_delete_book),
        ("Search Book", open_search_book),
        ("Issue Book", open_issue_book),
        ("Return Book", open_return_book),
        ("Manage Reservations", open_reservation),
        ("Reports", open_reports),
        ("Restore Deleted Book", open_undo_delete)
    ]

    for idx, (text, cmd) in enumerate(buttons):
        r = idx // 2
        c = idx % 2
        btn = ctk.CTkButton(btn_frame, text=text, width=190, height=40, font=("Segoe UI", 13, "bold"), command=cmd)
        btn.grid(row=r, column=c, padx=10, pady=10)

    ctk.CTkButton(root, text="Exit Application", fg_color="#DC2626", hover_color="#991B1B", width=400, height=40, font=("Segoe UI", 13, "bold"), command=root.destroy).pack(pady=25)
    root.mainloop()