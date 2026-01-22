import tkinter as tk

BG_MAIN = "#AADFE9"
BG_PANEL = "#2a2a40"
BTN_MAIN = "#4f46e5"
BTN_HOVER = "#6366f1"
TEXT_COLOR = "#ffffff"

def ui_button(parent, text, command, primary=True):
    bg = BTN_MAIN if primary else "#3b3b55"
    hover = BTN_HOVER if primary else "#4b4b6a"

    btn = tk.Frame(
        parent,
        bg=bg,
        height=46,
        cursor="hand2",
    )
    btn.pack_propagate(False)

    lbl = tk.Label(
        btn,
        text=text,
        bg=bg,
        fg="white",
        font=("Arial", 12, "bold"),
    )
    lbl.pack(expand=True)

    def on_enter(_):
        btn.config(bg=hover)
        lbl.config(bg=hover)

    def on_leave(_):
        btn.config(bg=bg)
        lbl.config(bg=bg)

    def on_click(_):
        command()

    for w in (btn, lbl):
        w.bind("<Enter>", on_enter)
        w.bind("<Leave>", on_leave)
        w.bind("<Button-1>", on_click)

    return btn


def ui_back_button(parent, text, command):
    bg = BG_PANEL
    hover_fg = "white"
    normal_fg = "#c7c9ff"

    btn = tk.Frame(parent, bg=bg, cursor="hand2")

    lbl = tk.Label(
        btn,
        text=f"← {text}",
        bg=bg,
        fg=normal_fg,
        font=("Arial", 11, "bold"),
    )
    lbl.pack()

    def on_enter(_):
        lbl.config(fg=hover_fg)

    def on_leave(_):
        lbl.config(fg=normal_fg)

    def on_click(_):
        if callable(command):
            command()

    for w in (btn, lbl):
        w.bind("<Enter>", on_enter)
        w.bind("<Leave>", on_leave)
        w.bind("<Button-1>", on_click)

    return btn


def draw_vertical_gradient(
    canvas: tk.Canvas,
    width: int,
    height: int,
    color1="#bfeef2",
    color2="#8fd3e8",
    steps=120
):
    canvas.delete("gradient")

    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)

    r_ratio = (r2 - r1) / steps
    g_ratio = (g2 - g1) / steps
    b_ratio = (b2 - b1) / steps

    for i in range(steps):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))

        color = f"#{nr//256:02x}{ng//256:02x}{nb//256:02x}"
        y1 = int((height / steps) * i)
        y2 = int((height / steps) * (i + 1))

        canvas.create_rectangle(
            0, y1, width, y2,
            outline="",
            fill=color,
            tags=("gradient",)
        )
