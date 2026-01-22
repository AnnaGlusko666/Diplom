import tkinter as tk
from tkinter import messagebox

from services.user_service import register_teacher
from ui.styles import *


def _add_placeholder(entry: tk.Entry, text: str):
    entry.insert(0, text)
    entry.config(fg="#9ca3af")  # сірий плейсхолдер

    def on_focus_in(_):
        if entry.get() == text:
            entry.delete(0, "end")
            entry.config(fg="#111827")

    def on_focus_out(_):
        if entry.get().strip() == "":
            entry.insert(0, text)
            entry.config(fg="#9ca3af")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


def _styled_entry(parent, is_password=False):
    e = tk.Entry(
        parent,
        bd=0,
        relief="flat",
        highlightthickness=2,
        highlightbackground="#3b3b55",
        highlightcolor=BTN_MAIN,
        font=("Arial", 12),
        fg="#111827",
        bg="#ffffff",
    )
    if is_password:
        e.config(show="•")
    return e


def register_teacher_screen(root, back):
    # фон
    frame = tk.Frame(root, bg=BG_MAIN)
    frame.pack(fill="both", expand=True)

    # щоб виглядало рівно по центру
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # "картка"
    card = tk.Frame(frame, bg=BG_PANEL, padx=28, pady=24)
    card.grid(row=0, column=0)

    title = tk.Label(
        card,
        text="Реєстрація вчителя",
        bg=BG_PANEL,
        fg=TEXT_COLOR,
        font=("Arial", 18, "bold"),
    )
    title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 18))

    # Логін
    tk.Label(
        card, text="Логін", bg=BG_PANEL, fg=TEXT_COLOR, font=("Arial", 11)
    ).grid(row=1, column=0, columnspan=2, sticky="w")

    login = _styled_entry(card)
    login.grid(row=2, column=0, columnspan=2, sticky="we", pady=(6, 14))
    _add_placeholder(login, "Наприклад: teacher01")

    # Пароль
    tk.Label(
        card, text="Пароль", bg=BG_PANEL, fg=TEXT_COLOR, font=("Arial", 11)
    ).grid(row=3, column=0, columnspan=2, sticky="w")

    password = _styled_entry(card, is_password=True)
    password.grid(row=4, column=0, sticky="we", pady=(6, 8))

    show_pwd = tk.BooleanVar(value=False)

    def toggle_password():
        if show_pwd.get():
            password.config(show="")
        else:
            password.config(show="•")

    toggle_btn = tk.Checkbutton(
        card,
        text="Показати",
        variable=show_pwd,
        command=toggle_password,
        bg=BG_PANEL,
        fg=TEXT_COLOR,
        activebackground=BG_PANEL,
        activeforeground=TEXT_COLOR,
        selectcolor=BG_PANEL,
        bd=0,
        font=("Arial", 10),
        cursor="hand2",
    )
    toggle_btn.grid(row=4, column=1, sticky="e", padx=(10, 0), pady=(6, 8))

    # Підтвердження
    tk.Label(
        card, text="Підтвердіть пароль", bg=BG_PANEL, fg=TEXT_COLOR, font=("Arial", 11)
    ).grid(row=5, column=0, columnspan=2, sticky="w")

    password2 = _styled_entry(card, is_password=True)
    password2.grid(row=6, column=0, columnspan=2, sticky="we", pady=(6, 10))

    # рядок помилки (гарніше, ніж тільки messagebox)
    error_lbl = tk.Label(card, text="", bg=BG_PANEL, fg="#fca5a5", font=("Arial", 10))
    error_lbl.grid(row=7, column=0, columnspan=2, sticky="w", pady=(0, 10))

    # кнопки
    btns = tk.Frame(card, bg=BG_PANEL)
    btns.grid(row=8, column=0, columnspan=2, sticky="we")
    btns.grid_columnconfigure(0, weight=1)
    btns.grid_columnconfigure(1, weight=1)

    def register():
        error_lbl.config(text="")

        l = login.get().strip()
        p1 = password.get()
        p2 = password2.get()

        # якщо плейсхолдер залишився
        if l == "" or l.startswith("Наприклад:"):
            error_lbl.config(text="Введіть логін.")
            return

        if len(p1) < 4:
            error_lbl.config(text="Пароль має бути мінімум 4 символи.")
            return

        if p1 != p2:
            error_lbl.config(text="Паролі не співпадають.")
            return

        if register_teacher(l, p1):
            messagebox.showinfo("Успіх", "Вчителя створено ✅")
            back()
        else:
            error_lbl.config(text="Такий логін уже зайнятий.")

    # ✅ КНОПКИ ТЕПЕР КАСТОМНІ (Frame+Label), тому macOS не зламає кольори
    back_btn = ui_button(btns, "Назад", back, primary=False)
    back_btn.grid(row=0, column=0, sticky="we", padx=(0, 10))

    reg_btn = ui_button(btns, "Зареєструвати", register, primary=True)
    reg_btn.grid(row=0, column=1, sticky="we", padx=(10, 0))

    # щоб інпути тягнулися вшир
    card.grid_columnconfigure(0, weight=1)
    card.grid_columnconfigure(1, weight=0)

    # фокус одразу на логін
    login.focus_set()
