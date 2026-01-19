"""
Вікно створення класу
"""

import tkinter as tk
from tkinter import messagebox
from styles import AppStyles

class CreateClassUI:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.styles = AppStyles
        
    def show(self):
        """Показати вікно створення класу"""
        # Очищення вікна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root,
                text="СТВОРЕННЯ КЛАСУ",
                font=self.styles.FONTS['title'],
                fg=self.styles.COLORS['primary'],
                bg=self.styles.COLORS['background']).pack(pady=30)
        
        form_frame = tk.Frame(self.root, bg=self.styles.COLORS['background'])
        form_frame.pack(pady=20)
        
        # ID вчителя
        tk.Label(form_frame,
                text="ID вчителя (класного керівника):",
                font=self.styles.FONTS['normal'],
                bg=self.styles.COLORS['background']).grid(row=0, column=0, pady=10, padx=10, sticky='e')
        
        self.teacher_id_entry = tk.Entry(form_frame, font=self.styles.FONTS['normal'], width=30)
        self.teacher_id_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Назва класу
        tk.Label(form_frame,
                text="Назва класу:",
                font=self.styles.FONTS['normal'],
                bg=self.styles.COLORS['background']).grid(row=1, column=0, pady=10, padx=10, sticky='e')
        
        self.class_name_entry = tk.Entry(form_frame, font=self.styles.FONTS['normal'], width=30)
        self.class_name_entry.grid(row=1, column=1, pady=10, padx=10)
        self.class_name_entry.insert(0, "10-А")
        
        button_frame = tk.Frame(self.root, bg=self.styles.COLORS['background'])
        button_frame.pack(pady=30)
        
        tk.Button(button_frame,
                 text="СТВОРИТИ КЛАС",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['success'],
                 fg='white',
                 width=20,
                 command=self.create_class).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame,
                 text="НАЗАД",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['secondary'],
                 fg='white',
                 width=15,
                 command=self.app.show_teacher_options).pack(side=tk.LEFT, padx=10)
    
    def create_class(self):
        """Створити новий клас"""
        teacher_id = self.teacher_id_entry.get()
        class_name = self.class_name_entry.get()
        
        if not teacher_id or not class_name:
            messagebox.showerror("Помилка", "Будь ласка, заповніть всі поля")
            return
        
        # Перевірка чи вчитель існує
        teacher = self.app.db.get_teacher_by_id(teacher_id)
        if not teacher:
            messagebox.showerror("Помилка", "Вчитель не знайдений!")
            return
        
        # Створення класу
        new_class = self.app.db.create_class(class_name, teacher_id)
        
        if new_class:
            messagebox.showinfo("Успіх", 
                              f"Клас '{class_name}' успішно створено!\nID класу: {new_class.id}")
            
            # Запит на створення учнів
            if messagebox.askyesno("Учні", "Бажаєте створити акаунти учнів зараз?"):
                self.app.show_generate_students(new_class.id)
            else:
                self.app.show_teacher_options()
        else:
            messagebox.showerror("Помилка", "Не вдалося створити клас")