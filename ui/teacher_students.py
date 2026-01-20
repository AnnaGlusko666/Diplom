import tkinter as tk
from ui.styles import *
from services.user_service import add_student

def teacher_students(root, teacher, back):
    frame = tk.Frame(root, bg=BG_MAIN)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Учні класу",
             bg=BG_MAIN, fg=TEXT_COLOR,
             font=("Arial", 16)).pack(pady=10)

    name_entry = tk.Entry(frame)
    name_entry.pack(pady=5)

    result = tk.Label(frame, bg=BG_MAIN, fg="lightgreen")
    result.pack(pady=5)

    def add():
        student = add_student(teacher["id"], name_entry.get())
        result.config(
            text=f"Логін: {student['login']} | Пароль: {student['password']}"
        )

    tk.Button(frame, text="Додати учня",
              bg=BTN_MAIN, fg="white",
              command=add).pack(pady=10)

    tk.Button(frame, text="Назад",
              command=back).pack(pady=20)
