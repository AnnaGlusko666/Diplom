import tkinter as tk
from ui.styles import BG_PANEL, TEXT_COLOR, ui_button


def role_screen(root, open_login):
    # очистити root
    for w in root.winfo_children():
        w.destroy()

    # --- ФОН: суцільний, як у картки ---
    frame = tk.Frame(root, bg=BG_PANEL)
    frame.pack(fill="both", expand=True)

    # щоб центр працював у fullscreen
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # --- Центральний контейнер ---
    content = tk.Frame(frame, bg=BG_PANEL)
    content.grid(row=0, column=0)

    # --- Заголовок ---
    title = tk.Label(
        content,
        text="Електронний журнал",
        bg=BG_PANEL,
        fg=TEXT_COLOR,
        font=("Arial", 50, "bold"),
    )
    title.pack(anchor="center", pady=(0, 12))

    # --- Опис (людяний, не технічний) ---
    subtitle = tk.Label(
        content,
        text=(
            "Зручний інструмент для навчання,\n"
            "контролю успішності та відвідування."
        ),
        bg=BG_PANEL,
        fg="#c7c9ff",
        font=("Arial",21),
        justify="center",
    )
    subtitle.pack(pady=(0, 28))

    # --- Маркери ---
    bullets = tk.Label(
        content,
        text=(
            "• Оцінки та результати навчання\n"
            "• Облік відвідування\n"
            "• Простий та зрозумілий інтерфейс"
        ),
        bg=BG_PANEL,
        fg="#b8b8d6",
        font=("Arial", 20),
        justify="left",
    )
    bullets.pack(pady=(0, 36))

    # --- Кнопки ---
    btns = tk.Frame(content, bg=BG_PANEL)
    btns.pack(fill="x")

    student_btn = ui_button(
        btns,
        "Я — учень",
        lambda: open_login("student"),
        primary=True,
    )
    student_btn.pack(fill="x", pady=(0, 14))

    teacher_btn = ui_button(
        btns,
        "Я — вчитель",
        lambda: open_login("teacher"),
        primary=False,
    )
    teacher_btn.pack(fill="x")

    # --- Підпис ---
    footer = tk.Label(
        content,
        text="Дипломний проєкт • 2026",
        bg=BG_PANEL,
        fg="#8f90b8",
        font=("Arial", 15),
    )
    footer.pack(pady=(32, 0))
