import tkinter as tk

from ui.background import create_background
from ui.styles import BG_PANEL, TEXT_COLOR, ui_button, draw_vertical_gradient


def role_screen(root, open_login):
    # очистити root
    for w in root.winfo_children():
        w.destroy()

    # --- ФОН: світлий градієнт (дружній, "освітній") ---
    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    def on_resize(event):
        # світлий фон
        draw_vertical_gradient(
            canvas,
            event.width,
            event.height,
            color1="#e8fbff",  # майже білий блакитний
            color2="#bfeef2",  # приємний блакитний
            steps=140
        )

        # центруємо картку
        canvas.coords(card_window, event.width // 2, event.height // 2)

    # --- КАРТКА (велика, не губиться у fullscreen) ---
    card = tk.Frame(canvas, bg=BG_PANEL, padx=90, pady=70)
    card_window = canvas.create_window(0, 0, window=card, anchor="center")

    canvas.bind("<Configure>", on_resize)

    # --- Контент картки ---
    title = tk.Label(
        card,
        text="Електронний журнал",
        bg=BG_PANEL,
        fg=TEXT_COLOR,
        font=("Arial", 28, "bold"),
    )
    title.grid(row=0, column=0, sticky="w", pady=(0, 10))

    subtitle = tk.Label(
        card,
        text="Зручна система для обліку оцінок, відвідування та прогресу навчання.",
        bg=BG_PANEL,
        fg="#c7c9ff",
        font=("Arial", 13),
        justify="left",
        wraplength=520,
    )
    subtitle.grid(row=1, column=0, sticky="w", pady=(0, 24))

    # --- Маркери переваг ---
    bullets = tk.Label(
        card,
        text="• Оцінки та результати\n• Відвідування\n• Швидкий доступ до журналу",
        bg=BG_PANEL,
        fg="#b8b8d6",
        font=("Arial", 12),
        justify="left",
    )
    bullets.grid(row=2, column=0, sticky="w", pady=(0, 28))

    # --- Блок кнопок ---
    btns = tk.Frame(card, bg=BG_PANEL)
    btns.grid(row=3, column=0, sticky="we")
    btns.grid_columnconfigure(0, weight=1)

    # великі кнопки
    student_btn = ui_button(btns, "Я — учень", lambda: open_login("student"), primary=True)
    student_btn.grid(row=0, column=0, sticky="we", pady=(0, 14))

    teacher_btn = ui_button(btns, "Я — вчитель", lambda: open_login("teacher"), primary=False)
    teacher_btn.grid(row=1, column=0, sticky="we")

    # --- Нижній підпис (виглядає “доросло”) ---
    footer = tk.Label(
        card,
        text="Дипломний проєкт • 2026",
        bg=BG_PANEL,
        fg="#8f90b8",
        font=("Arial", 10),
    )
    footer.grid(row=4, column=0, sticky="w", pady=(26, 0))

    card.grid_columnconfigure(0, weight=1)
