import tkinter as tk
from tkinter import messagebox

from ui.styles import BG_PANEL, TEXT_COLOR, BTN_MAIN, ui_button, ui_back_button


def login_screen(root, role, on_panel, on_register, back_to_roles):
    # очистити root
    for w in root.winfo_children():
        w.destroy()

    # фон
    frame = tk.Frame(root, bg=BG_PANEL)
    frame.pack(fill="both", expand=True)

    # центрування
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # ✅ wrapper — центр
    wrapper = tk.Frame(frame, bg=BG_PANEL)
    wrapper.grid(row=0, column=0)

    # ✅ box — фіксована ширина
    box = tk.Frame(wrapper, bg=BG_PANEL)
    box.pack()

    # задаємо ширину через "порожні" колонки (стабільно для Tk)
    box.grid_columnconfigure(0, minsize=520)  # ⬅️ ширина форми

    # Контент кладемо у grid, щоб усе тягнулось по ширині
    back_btn = ui_back_button(box, "Назад", back_to_roles)
    back_btn.grid(row=0, column=0, sticky="w", pady=(0, 18))

    title = tk.Label(
        box, text="Вхід",
        bg=BG_PANEL, fg=TEXT_COLOR,
        font=("Arial", 40, "bold"),
    )
    title.grid(row=1, column=0, sticky="w", pady=(0, 24))

    if role == "teacher":
        reg_btn = ui_button(box, "Реєстрація вчителя", on_register, primary=False)
        reg_btn.grid(row=8, column=0, sticky="we", pady=(12, 0), ipady=4)

    # helper entry
    def styled_entry(parent, show=None):
        e = tk.Entry(
            parent,
            bd=0,
            relief="flat",
            highlightthickness=2,
            highlightbackground="#3b3b55",
            highlightcolor=BTN_MAIN,
            bg="white",
            fg="#111827",
            font=("Arial", 16),
        )
        if show:
            e.config(show=show)
        return e

    tk.Label(box, text="Логін", bg=BG_PANEL, fg=TEXT_COLOR, font=("Arial", 21)).grid(
        row=2, column=0, sticky="w"
    )
    login_entry = styled_entry(box)
    login_entry.grid(row=3, column=0, sticky="we", pady=(8, 18), ipady=10)

    tk.Label(box, text="Пароль", bg=BG_PANEL, fg=TEXT_COLOR, font=("Arial", 21)).grid(
        row=4, column=0, sticky="w"
    )
    pass_entry = styled_entry(box, show="•")
    pass_entry.grid(row=5, column=0, sticky="we", pady=(8, 10), ipady=10)

    show_pwd = tk.BooleanVar(value=False)

    def toggle_pwd():
        pass_entry.config(show="" if show_pwd.get() else "•")

    chk = tk.Checkbutton(
        box,
        text="Показати пароль",
        variable=show_pwd,
        command=toggle_pwd,
        bg=BG_PANEL,
        fg=TEXT_COLOR,
        activebackground=BG_PANEL,
        activeforeground=TEXT_COLOR,
        selectcolor=BG_PANEL,
        bd=0,
        font=("Arial", 15),
        cursor="hand2",
    )
    chk.grid(row=6, column=0, sticky="w", pady=(0, 18))

    def do_login():
        login = login_entry.get().strip()
        password = pass_entry.get()

        if not login or not password:
            messagebox.showwarning("Помилка", "Введіть логін і пароль.")
            return

        # тут твоя реальна логіка входу має бути
        on_panel(role, {"login": login, "password": password})

    btn = ui_button(box, "Увійти", do_login, primary=True)
    btn.grid(row=7, column=0, sticky="we", ipady=4, pady=(10, 0))

    login_entry.focus_set()
