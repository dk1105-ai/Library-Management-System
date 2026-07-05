import customtkinter as ctk
from database import conn, cursor
from theme import TITLE_FONT

def open_window():
    win = ctk.CTk()
    win.title("Data Engine Metrics View")
    win.geometry("450x450")
    win.resizable(False, False)

    ctk.CTkLabel(win, text="Analytics Reports", font=TITLE_FONT).pack(pady=(40, 20))
    
    card_frame = ctk.CTkFrame(win, corner_radius=12, width=340)
    card_frame.pack(fill="both", expand=True, padx=40, pady=10)

    metrics_layout = [
        ("Total Books Tracked", "tb"),
        ("Active Leases Out", "ib"),
        ("Net Stock Present", "ab"),
        ("Enrolled Students", "ts")
    ]
    ui_hooks = {}

    for label_str, key in metrics_layout:
        f = ctk.CTkFrame(card_frame, fg_color="transparent")
        f.pack(fill="x", padx=25, pady=12)
        ctk.CTkLabel(f, text=label_str, font=("Segoe UI", 13, "bold"), anchor="w").pack(side="left")
        v = ctk.CTkLabel(f, text="0", font=("Segoe UI", 15, "bold"), text_color="#3B82F6")
        v.pack(side="right")
        ui_hooks[key] = v

    def refresh_metrics():
        cursor.execute("SELECT COUNT(*) FROM Book")
        ui_hooks["tb"].configure(text=str(cursor.fetchone()[0]))

        cursor.execute("SELECT COUNT(*) FROM Issue_Book WHERE return_date IS NULL")
        ui_hooks["ib"].configure(text=str(cursor.fetchone()[0]))

        cursor.execute("SELECT SUM(available) FROM Book")
        avail = cursor.fetchone()[0]
        ui_hooks["ab"].configure(text=str(avail if avail else 0))

        cursor.execute("SELECT COUNT(*) FROM Student")
        ui_hooks["ts"].configure(text=str(cursor.fetchone()[0]))

    ctk.CTkButton(win, text="Refresh Report Data", width=340, height=42, corner_radius=8, font=("Segoe UI", 13, "bold"), command=refresh_metrics).pack(pady=25)
    refresh_metrics()
    win.mainloop()