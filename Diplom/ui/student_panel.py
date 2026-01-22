import tkinter as tk
from ui.styles import *

def student_panel(root, student):
    frame = tk.Frame(root, bg=BG_MAIN)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text=f"Учень: {student['name']}",
             bg=BG_MAIN, fg=TEXT_COLOR,
             font=("Arial", 16)).pack(pady=30)

    for text in ["Оцінки", "Розклад", "Мотивація", "Магазин", "Профіль"]:
        tk.Button(frame, text=text, bg=BTN_MAIN, fg="white").pack(pady=5)
