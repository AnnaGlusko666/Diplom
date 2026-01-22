import tkinter as tk
from services.user_service import auth_teacher, auth_student
from ui.styles import (
    BG_MAIN,
    BG_PANEL,
    TEXT_COLOR,
    BTN_MAIN,
    BTN_HOVER,
    ui_button,
    ui_back_button,
)
from ui.background import create_background


def styled_entry(parent, is_password=False):
    entry = tk.Entry(
        parent,
        bd=0,
        relief="flat",
        highlightthickness=2,
        highlightbackground="#3b3b55",
        highlightcolor=BTN_MAIN,
        bg="white",
        fg="#111827",
        font=("Arial", 12),
    )
    if is_password:
        entry.config(show="•")
    return entry


def login_screen(
    root,
    role: str,
    open_panel,
    open_register,
    back_to_roles,
):
    # Очистити root
    for w in root.winfo_children():
        w.destroy()

    # Фон
    outer = create_background(root)

    card = tk.Frame(outer, bg=BG_PANEL, padx=50, pady=40)
    card_window = outer.create_window(0, 0, window=card, anchor="center")

    def center_card(event):
        outer.coords(card_window, event.width // 2, event.height // 2)

    outer.bind("<Configure>", center_card)

    outer.grid_rowconfigure(0, weight=1)
    outer.grid_columnconfigure(0, weight=1)

    # Картка
    card = tk.Frame(outer, bg=BG_PANEL, padx=40, pady=32)
    card.grid(row=0, column=0)

    # ===== ROW 0 — НАЗАД =====
    back_btn = ui_back_button(card, "Назад", back_to_roles)
    back_btn.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 18))

    # ===== ROW 1 — ЗАГОЛОВОК =====
    title = tk.Label(
        card,
        text="Вхід",
        bg=BG_PANEL,
        fg=TEXT_COLOR,
        font=("Arial", 22, "bold"),
    )
    title.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 24))

    # ===== ROW 2 — ЛОГІН (LABEL) =====
    tk.Label(
        card,
        text="Логін",
        bg=BG_PANEL,
        fg=TEXT_COLOR,
        font=("Arial", 12),
    ).grid(row=2, column=0, columnspan=2, sticky="w")

    # ===== ROW 3 — ЛОГІН (ENTRY) =====
    login_entry = styled_entry(card)
    login_entry.grid(
        row=3,
        column=0,
        columnspan=2,
        sticky="we",
        pady=(8, 20),
    )

    # ===== ROW 4 — ПАРОЛЬ (LABEL) =====
    tk.Label(
        card,
        text="Пароль",
        bg=BG_PANEL,
        fg=TEXT_COLOR,
        font=("Arial", 12),
    ).grid(row=4, column=0, columnspan=2, sticky="w")

    # ===== ROW 5 — ПАРОЛЬ (ENTRY + CHECKBOX) =====
    password_entry = styled_entry(card, is_password=True)
    password_entry.grid(row=5, column=0, sticky="we", pady=(8, 10))

    show_pwd = tk.BooleanVar(value=False)

    def toggle_password():
        password_entry.config(show="" if show_pwd.get() else "•")

    toggle = tk.Checkbutton(
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
        cursor="hand2",
        font=("Arial", 11),
    )
    toggle.grid(row=5, column=1, sticky="e", padx=(14, 0))

    # ===== ROW 6 — ПОМИЛКА =====
    error_lbl = tk.Label(
        card,
        text="",
        bg=BG_PANEL,
        fg="#fca5a5",
        font=("Arial", 11),
    )
    error_lbl.grid(row=6, column=0, columnspan=2, sticky="w", pady=(0, 16))

    # ===== ROW 7 — КНОПКИ =====
    btns = tk.Frame(card, bg=BG_PANEL)
    btns.grid(row=7, column=0, columnspan=2, sticky="we")

    def do_login():
        error_lbl.config(text="")

        login = login_entry.get().strip()
        password = password_entry.get()

        if not login:
            error_lbl.config(text="Введіть логін.")
            return

        if not password:
            error_lbl.config(text="Введіть пароль.")
            return

        if role == "teacher":
            user = auth_teacher(login, password)
        else:
            user = auth_student(login, password)

        if not user:
            error_lbl.config(text="Невірний логін або пароль.")
            return

        open_panel(role, user)

    login_btn = ui_button(btns, "Увійти", do_login, primary=True)
    login_btn.pack(fill="x")

    if role == "teacher":
        reg_btn = ui_button(
            btns,
            "Реєстрація вчителя",
            open_register,
            primary=False,
        )
        reg_btn.pack(fill="x", pady=(14, 0))

    # ===== GRID CONFIG =====
    card.grid_columnconfigure(0, weight=1)
    card.grid_columnconfigure(1, weight=0)

    login_entry.focus_set()
