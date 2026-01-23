import tkinter as tk
from tkinter import messagebox

from services.user_service import register_teacher
from ui.styles import *


def _add_placeholder(entry: tk.Entry, text: str):
    entry.insert(0, text)
    entry.config(fg="#9ca3af")

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
        font=("Arial", 16),
        fg="#111827",
        bg="#ffffff",
    )
    if is_password:
        e.config(show="•")
    return e


def register_teacher_screen(root, back):
    frame = tk.Frame(root, bg=BG_PANEL)
    frame.pack(fill="both", expand=True)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    card = tk.Frame(frame, bg=BG_PANEL, padx=60, pady=50)
    card.grid(row=0, column=0)

    card.configure(width=720, height=620)   # ⬅️ висоту зробив трохи більшу
    card.grid_propagate(False)

    # щоб поля тягнулись
    card.grid_columnconfigure(0, weight=1)

    # ====== ROW COUNTER (щоб не плутатись) ======
    r = 0

    # Заголовок
    title = tk.Label(
        card,
        text="Реєстрація вчителя",
        bg=BG_PANEL,
        fg=TEXT_COLOR,
        font=("Arial", 26, "bold"),
    )
    title.grid(row=r, column=0, sticky="w", pady=(0, 26))
    r += 1

    # Логін
    tk.Label(
        card,
        text="Логін",
        bg=BG_PANEL,
        fg=TEXT_COLOR,
        font=("Arial", 21),
    ).grid(row=r, column=0, sticky="w")
    r += 1

    login = _styled_entry(card)
    login.grid(row=r, column=0, sticky="we", pady=(10, 22), ipady=10)
    _add_placeholder(login, "Наприклад: teacher01")
    r += 1

    # Пароль
    tk.Label(
        card,
        text="Пароль",
        bg=BG_PANEL,
        fg=TEXT_COLOR,
        font=("Arial", 21),
    ).grid(row=r, column=0, sticky="w")
    r += 1

    password = _styled_entry(card, is_password=True)
    password.grid(row=r, column=0, sticky="we", pady=(10, 6), ipady=10)
    r += 1

    show_pwd1 = tk.BooleanVar(value=False)

    def toggle_pwd_1():
        password.config(show="" if show_pwd1.get() else "•")

    toggle_1 = tk.Checkbutton(
        card,
        text="Показати пароль",
        variable=show_pwd1,
        command=toggle_pwd_1,
        bg=BG_PANEL,
        fg=TEXT_COLOR,
        activebackground=BG_PANEL,
        activeforeground=TEXT_COLOR,
        selectcolor=BG_PANEL,
        bd=0,
        font=("Arial", 15),
        cursor="hand2",
    )
    toggle_1.grid(row=r, column=0, sticky="w", pady=(0, 18))
    r += 1

    # Підтвердження
    tk.Label(
        card,
        text="Підтвердіть пароль",
        bg=BG_PANEL,
        fg=TEXT_COLOR,
        font=("Arial", 21),
    ).grid(row=r, column=0, sticky="w")
    r += 1

    password2 = _styled_entry(card, is_password=True)
    password2.grid(row=r, column=0, sticky="we", pady=(10, 6), ipady=10)
    r += 1

    show_pwd2 = tk.BooleanVar(value=False)

    def toggle_pwd_2():
        password2.config(show="" if show_pwd2.get() else "•")

    toggle_2 = tk.Checkbutton(
        card,
        text="Показати пароль",
        variable=show_pwd2,
        command=toggle_pwd_2,
        bg=BG_PANEL,
        fg=TEXT_COLOR,
        activebackground=BG_PANEL,
        activeforeground=TEXT_COLOR,
        selectcolor=BG_PANEL,
        bd=0,
        font=("Arial", 15),
        cursor="hand2",
    )
    toggle_2.grid(row=r, column=0, sticky="w", pady=(0, 20))
    r += 1

    # Помилка
    error_lbl = tk.Label(
        card,
        text="",
        bg=BG_PANEL,
        fg="#fca5a5",
        font=("Arial", 12, "bold"),
    )
    error_lbl.grid(row=r, column=0, sticky="w", pady=(0, 20))
    r += 1

    # Кнопки
    btns = tk.Frame(card, bg=BG_PANEL)
    btns.grid(row=r, column=0, sticky="we", pady=(10, 0))
    btns.grid_columnconfigure(0, weight=1)
    btns.grid_columnconfigure(1, weight=1)

    def register():
        error_lbl.config(text="")

        l = login.get().strip()
        p1 = password.get()
        p2 = password2.get()

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

    back_btn = ui_button(btns, "Назад", back, primary=False)
    back_btn.grid(row=0, column=0, sticky="we", padx=(0, 12))

    reg_btn = ui_button(btns, "Зареєструвати", register, primary=True)
    reg_btn.grid(row=0, column=1, sticky="we", padx=(12, 0))

    login.focus_set()
