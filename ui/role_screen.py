import tkinter as tk
from ui.styles import *

def role_screen(root, open_login):
    frame = tk.Frame(root, bg=BG_MAIN)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Електронний журнал",
             font=("Arial", 18, "bold"),
             bg=BG_MAIN, fg=TEXT_COLOR).pack(pady=30)

    tk.Button(frame, text="Учень", bg=BTN_MAIN, fg="white",
              command=lambda: open_login("student")).pack(pady=10, ipadx=20, ipady=5)

    tk.Button(frame, text="Вчитель", bg=BTN_MAIN, fg="white",
              command=lambda: open_login("teacher")).pack(pady=10, ipadx=20, ipady=5)
