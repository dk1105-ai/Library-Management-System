import customtkinter as ctk
from tkinter import messagebox
from database import conn, cursor
from theme import TITLE_FONT, LABEL_FONT

def login_action(root, user_entry, pass_entry):
    username = user_entry.get()
    password = pass_entry.get()

    query = "SELECT * FROM Admin WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Success", "Login Successful")
        root.destroy()
        # Open Dashboard cleanly
        import dashboard
        dashboard.start_dashboard()
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

def toggle_password_visibility(pass_entry, toggle_btn):
    if pass_entry.cget("show") == "*":
        pass_entry.configure(show="")
        toggle_btn.configure(text="🙈")
    else:
        pass_entry.configure(show="*")
        toggle_btn.configure(text="👁")

def start_login():
    root = ctk.CTk()
    root.title("System Login")
    root.geometry("400x450")
    root.resizable(False, False)

    title = ctk.CTkLabel(root, text="📚 Smart Library System", font=TITLE_FONT)
    title.pack(pady=(40, 30))

    user_label = ctk.CTkLabel(root, text="Username", font=LABEL_FONT)
    user_label.pack(anchor="w", padx=60)
    user_entry = ctk.CTkEntry(root, width=280, height=40, placeholder_text="Enter Username")
    user_entry.pack(pady=(5, 15))

    pass_label = ctk.CTkLabel(root, text="Password", font=LABEL_FONT)
    pass_label.pack(anchor="w", padx=60)

# Frame for password entry and eye button
    pass_frame = ctk.CTkFrame(root, fg_color="transparent")
    pass_frame.pack(pady=(5, 30))

    pass_entry = ctk.CTkEntry(
       pass_frame,
        width=240,
       height=40,
    placeholder_text="Enter Password",
    show="*"
)
    pass_entry.pack(side="left")

    toggle_btn = ctk.CTkButton(
    pass_frame,
    text="👁",
    width=35,
    height=40,
    fg_color="transparent",
    command=lambda: toggle_password_visibility(pass_entry, toggle_btn)
)
    toggle_btn.pack(side="left", padx=(5, 0))

    login_btn = ctk.CTkButton(root, text="Login", width=280, height=42, corner_radius=8, font=(TITLE_FONT[0], 14, "bold"), command=lambda: login_action(root, user_entry, pass_entry))
    login_btn.pack()

    root.mainloop()


    