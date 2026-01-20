import tkinter as tk

from ui.role_screen import role_screen
from ui.login_screen import login_screen
from ui.register_teacher import register_teacher_screen
from ui.teacher_panel import teacher_panel
from ui.teacher_students import teacher_students
from ui.student_panel import student_panel


def open_teacher_panel(teacher):
    clear()
    teacher_panel(root, teacher, lambda: open_teacher_students(teacher))

def open_teacher_students(teacher):
    clear()
    teacher_students(root, teacher, lambda: open_teacher_panel(teacher))


root = tk.Tk()
root.title("Електронний журнал")
root.geometry("500x400")


def clear():
    for w in root.winfo_children():
        w.destroy()


def open_login(role):
    clear()
    login_screen(root, role, open_panel, open_register)


def open_register():
    clear()
    register_teacher_screen(root, lambda: open_login("teacher"))


def open_panel(role, user):
    clear()
    if role == "teacher":
        open_teacher_panel(user)
    else:
        student_panel(root, user)



role_screen(root, open_login)
root.mainloop()
