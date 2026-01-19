"""
Модуль для виставлення оцінок вчителем
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models import Grade, generate_id
from database import Database
from motivation import MotivationSystem
from styles import AppStyles

class AddGradeUI:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.styles = AppStyles
        self.motivation = MotivationSystem(app_instance.db)
        
    def show(self):
        """Показати вікно виставлення оцінки"""
        self.grade_window = tk.Toplevel(self.root)
        self.grade_window.title("Виставлення оцінки")
        self.grade_window.geometry("600x500")
        self.grade_window.configure(bg=self.styles.COLORS['background'])
        
        tk.Label(self.grade_window,
                text="📝 ВИСТАВЛЕННЯ ОЦІНКИ",
                font=self.styles.FONTS['title'],
                fg=self.styles.COLORS['primary'],
                bg=self.styles.COLORS['background']).pack(pady=20)
        
        # Отримуємо класи вчителя
        classes = self.app.db.get_teacher_classes(self.app.current_user.id)
        
        if not classes:
            tk.Label(self.grade_window,
                    text="У вас немає класів для виставлення оцінок",
                    font=self.styles.FONTS['normal'],
                    fg=self.styles.COLORS['secondary'],
                    bg=self.styles.COLORS['background']).pack(pady=50)
            return
        
        # Вибор класу
        self.create_class_selection(classes)
    
    def create_class_selection(self, classes):
        """Створити вибір класу"""
        tk.Label(self.grade_window,
                text="Оберіть клас:",
                font=self.styles.FONTS['normal'],
                bg=self.styles.COLORS['background']).pack(pady=10)
        
        self.class_var = tk.StringVar()
        class_combobox = ttk.Combobox(self.grade_window, 
                                     textvariable=self.class_var,
                                     values=[c.name for c in classes],
                                     state='readonly',
                                     width=30)
        class_combobox.pack(pady=5)
        class_combobox.current(0)
        
        # Кнопка продовжити
        tk.Button(self.grade_window,
                 text="ОБРАТИ КЛАС",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['primary'],
                 fg='white',
                 command=lambda: self.show_student_selection(classes[class_combobox.current()].id)).pack(pady=20)
    
    def show_student_selection(self, class_id):
        """Показати вибір учня"""
        # Очистити вікно
        for widget in self.grade_window.winfo_children():
            widget.destroy()
        
        tk.Label(self.grade_window,
                text="📝 ВИСТАВЛЕННЯ ОЦІНКИ",
                font=self.styles.FONTS['title'],
                fg=self.styles.COLORS['primary'],
                bg=self.styles.COLORS['background']).pack(pady=20)
        
        # Отримати учнів класу
        students = self.app.db.get_students_in_class(class_id)
        
        if not students:
            tk.Label(self.grade_window,
                    text="У класі немає учнів",
                    font=self.styles.FONTS['normal'],
                    fg=self.styles.COLORS['secondary'],
                    bg=self.styles.COLORS['background']).pack(pady=50)
            return
        
        # Вибор учня
        tk.Label(self.grade_window,
                text="Оберіть учня:",
                font=self.styles.FONTS['normal'],
                bg=self.styles.COLORS['background']).pack(pady=10)
        
        self.student_var = tk.StringVar()
        student_names = [f"{s.full_name} ({s.username})" for s in students]
        student_combobox = ttk.Combobox(self.grade_window, 
                                       textvariable=self.student_var,
                                       values=student_names,
                                       state='readonly',
                                       width=40)
        student_combobox.pack(pady=5)
        student_combobox.current(0)
        
        # Вибор предмету
        tk.Label(self.grade_window,
                text="Оберіть предмет:",
                font=self.styles.FONTS['normal'],
                bg=self.styles.COLORS['background']).pack(pady=10)
        
        self.subject_var = tk.StringVar()
        subjects = ["Математика", "Українська мова", "Історія", "Фізика", 
                   "Хімія", "Біологія", "Англійська мова", "Географія", 
                   "Інформатика", "Фізкультура", "Мистецтво"]
        
        subject_combobox = ttk.Combobox(self.grade_window, 
                                       textvariable=self.subject_var,
                                       values=subjects,
                                       state='readonly',
                                       width=30)
        subject_combobox.pack(pady=5)
        subject_combobox.current(0)
        
        # Оцінка
        tk.Label(self.grade_window,
                text="Оцінка (1-12):",
                font=self.styles.FONTS['normal'],
                bg=self.styles.COLORS['background']).pack(pady=10)
        
        self.grade_var = tk.StringVar()
        grade_spinbox = tk.Spinbox(self.grade_window,
                                  from_=1, to=12,
                                  textvariable=self.grade_var,
                                  width=10,
                                  font=self.styles.FONTS['normal'])
        grade_spinbox.pack(pady=5)
        self.grade_var.set("10")
        
        # Коментар
        tk.Label(self.grade_window,
                text="Коментар (необов'язково):",
                font=self.styles.FONTS['normal'],
                bg=self.styles.COLORS['background']).pack(pady=10)
        
        self.comment_text = tk.Text(self.grade_window, height=4, width=50)
        self.comment_text.pack(pady=5)
        
        # Збереження ID для подальшого використання
        self.selected_class_id = class_id
        self.selected_students = students
        
        # Кнопка виставлення оцінки
        tk.Button(self.grade_window,
                 text="ВИСТАВИТИ ОЦІНКУ",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['success'],
                 fg='white',
                 command=self.add_grade).pack(pady=20)
    
    def add_grade(self):
        """Додати оцінку"""
        try:
            # Отримуємо дані
            student_index = self.student_var.get().split('(')[-1].replace(')', '')
            student = None
            for s in self.selected_students:
                if s.username in student_index:
                    student = s
                    break
            
            if not student:
                messagebox.showerror("Помилка", "Учень не знайдений")
                return
            
            subject = self.subject_var.get()
            grade_value = int(self.grade_var.get())
            comment = self.comment_text.get("1.0", tk.END).strip()
            
            # Перевірка валідності
            if not 1 <= grade_value <= 12:
                messagebox.showerror("Помилка", "Оцінка повинна бути від 1 до 12")
                return
            
            # Створюємо оцінку
            new_grade = Grade(
                id=generate_id(),
                student_id=student.id,
                teacher_id=self.app.current_user.id,
                subject=subject,
                value=grade_value,
                date=datetime.now().isoformat(),
                comment=comment if comment else None
            )
            
            # Додаємо оцінку з мотиваційною системою
            if self.motivation.add_grade_with_motivation(new_grade):
                messagebox.showinfo("Успіх", 
                                  f"Оцінку {grade_value} успішно виставлено!\n"
                                  f"Учень: {student.full_name}\n"
                                  f"Предмет: {subject}")
                self.grade_window.destroy()
            else:
                messagebox.showerror("Помилка", "Не вдалося виставити оцінку")
                
        except ValueError:
            messagebox.showerror("Помилка", "Будь ласка, введіть коректну оцінку")
        except Exception as e:
            messagebox.showerror("Помилка", f"Сталася помилка: {str(e)}")