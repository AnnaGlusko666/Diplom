import tkinter as tk
from tkinter import messagebox
from services.user_service import register_teacher
from ui.styles import *

def register_teacher_screen(root, back):
    frame = tk.Frame(root, bg=BG_PANEL)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Реєстрація вчителя",
             bg=BG_PANEL, fg=TEXT_COLOR,
             font=("Arial", 16)).pack(pady=20)

    login = tk.Entry(frame)
    login.pack(pady=5)

    password = tk.Entry(frame, show="*")
    password.pack(pady=5)

    def register():
        if register_teacher(login.get(), password.get()):
            messagebox.showinfo("Успіх", "Вчителя створено")
            back()
        else:
            messagebox.showerror("Помилка", "Логін зайнятий")

    tk.Button(frame, text="Зареєструвати", bg=BTN_MAIN, fg="white",
              command=register).pack(pady=10)
