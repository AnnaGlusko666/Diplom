"""
Вікно перегляду учнів класу
"""

import tkinter as tk
from tkinter import ttk
from styles import AppStyles

class ClassStudentsUI:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.styles = AppStyles
        
    def show(self, class_id, class_name):
        """Показати учнів класу"""
        students = self.app.db.get_students_in_class(class_id)
        
        self.students_window = tk.Toplevel(self.root)
        self.students_window.title(f"Учні класу {class_name}")
        self.students_window.geometry("700x500")
        self.students_window.configure(bg=self.styles.COLORS['background'])
        
        tk.Label(self.students_window,
                text=f"👥 УЧНІ КЛАСУ {class_name}",
                font=self.styles.FONTS['title'],
                fg=self.styles.COLORS['primary'],
                bg=self.styles.COLORS['background']).pack(pady=20)
        
        if not students:
            tk.Label(self.students_window,
                    text="У класі ще немає учнів",
                    font=self.styles.FONTS['normal'],
                    fg=self.styles.COLORS['secondary'],
                    bg=self.styles.COLORS['background']).pack(pady=50)
        else:
            # Таблиця учнів
            self.create_students_table(students)
    
    def create_students_table(self, students):
        """Створити таблицю учнів"""
        tree_frame = tk.Frame(self.students_window, bg=self.styles.COLORS['background'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Створення Treeview
        tree = ttk.Treeview(tree_frame, columns=('ID', 'Ім\'я', 'Логін'), show='headings')
        
        # Налаштування колонок
        tree.heading('ID', text='ID')
        tree.heading('Ім\'я', text='Ім\'я')
        tree.heading('Логін', text='Логін')
        
        tree.column('ID', width=100)
        tree.column('Ім\'я', width=200)
        tree.column('Логін', width=150)
        
        # Додавання даних
        for student in students:
            tree.insert('', tk.END, values=(student.id, student.full_name, student.username))
        
        # Прокрутка
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)