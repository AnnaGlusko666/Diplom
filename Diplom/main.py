import tkinter as tk

from ui.role_screen import role_screen
from ui.login_screen import login_screen
from ui.register_teacher import register_teacher_screen
from ui.teacher_panel import teacher_panel
from ui.teacher_students import teacher_students
from ui.student_panel import student_panel


root = tk.Tk()
root.title("Електронний журнал")

root.state("zoomed")  # Windows / Linux

root.configure(bg="black")  # щоб не було білих миготінь





def clear():
    for w in root.winfo_children():
        w.destroy()


# ✅ ПОВЕРНЕННЯ НА ЕКРАН ВИБОРУ РОЛІ
def show_role_select():
    clear()
    role_screen(root, open_login)


def open_teacher_panel(teacher):
    clear()
    teacher_panel(root, teacher, lambda: open_teacher_students(teacher))


def open_teacher_students(teacher):
    clear()
    teacher_students(root, teacher, lambda: open_teacher_panel(teacher))


def open_panel(role, user):
    clear()
    if role == "teacher":
        open_teacher_panel(user)
    else:
        student_panel(root, user)


# ✅ show_role_select — це callback для кнопки "Назад"
def open_login(role, back_to_roles=None):
    clear()
    if back_to_roles is None:
        back_to_roles = show_role_select  # дефолтно "Назад" веде на role_screen

    login_screen(root, role, open_panel, open_register, back_to_roles)


def open_register():
    clear()
    # ✅ Назад з реєстрації повертає на логін вчителя
    register_teacher_screen(root, lambda: open_login("teacher", show_role_select))


# ✅ стартова сторінка
show_role_select()
root.mainloop()
