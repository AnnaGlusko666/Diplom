import tkinter as tk
from ui.styles import draw_vertical_gradient, BG_PANEL

def create_background(root):
    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    def on_resize(event):
        draw_vertical_gradient(canvas, event.width, event.height)

    canvas.bind("<Configure>", on_resize)
    return canvas
