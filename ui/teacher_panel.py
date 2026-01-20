import tkinter as tk
from ui.styles import *
from services.user_service import add_student

def teacher_panel(root, teacher, open_students):
    frame = tk.Frame(root, bg=BG_MAIN)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text=f"Вчитель: {teacher['login']}",
        bg=BG_MAIN,
        fg=TEXT_COLOR,
        font=("Arial", 16)
    ).pack(pady=20)

    tk.Button(frame, text="Учні", bg=BTN_MAIN, fg="white",
              command=open_students).pack(pady=10, ipadx=20, ipady=5)

    tk.Button(frame, text="Оцінки", bg=BTN_MAIN, fg="white").pack(pady=5)
    tk.Button(frame, text="Мотивація", bg=BTN_MAIN, fg="white").pack(pady=5)
    tk.Button(frame, text="Магазин вчителя", bg=BTN_MAIN, fg="white").pack(pady=5)

    tk.Button(frame, text="Вийти", command=root.quit).pack(pady=20)
