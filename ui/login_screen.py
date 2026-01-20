import tkinter as tk
from tkinter import messagebox
from services.user_service import auth_teacher, auth_student
from ui.styles import *

def login_screen(root, role, open_panel, open_register):
    frame = tk.Frame(root, bg=BG_PANEL)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Вхід",
             font=("Arial", 16),
             bg=BG_PANEL, fg=TEXT_COLOR).pack(pady=20)

    login = tk.Entry(frame)
    login.pack(pady=5)

    password = tk.Entry(frame, show="*")
    password.pack(pady=5)

    def login_action():
        if role == "teacher":
            user = auth_teacher(login.get(), password.get())
        else:
            user = auth_student(login.get(), password.get())

        if user:
            open_panel(role, user)
        else:
            messagebox.showerror("Помилка", "Невірні дані")

    tk.Button(frame, text="Увійти", bg=BTN_MAIN, fg="white",
              command=login_action).pack(pady=10)

    if role == "teacher":
        tk.Button(frame, text="Реєстрація вчителя",
                  command=open_register).pack()
