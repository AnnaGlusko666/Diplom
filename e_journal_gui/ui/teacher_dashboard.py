"""
Панель управління для вчителя - ОНОВЛЕНИЙ
"""

import tkinter as tk
from styles import AppStyles

class TeacherDashboard:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.styles = AppStyles
        
    def show(self):
        """Показати панель вчителя"""
        # Очищення вікна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Верхня панель
        header_frame = tk.Frame(self.root, bg=self.styles.COLORS['primary'], height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame,
                text=f"👨‍🏫 {self.app.current_user.full_name}",
                font=self.styles.FONTS['title'],
                fg='white',
                bg=self.styles.COLORS['primary']).pack(side=tk.LEFT, padx=30, pady=20)
        
        tk.Label(header_frame,
                text="ВЧИТЕЛЬ",
                font=self.styles.FONTS['header'],
                fg='white',
                bg=self.styles.COLORS['primary']).pack(side=tk.RIGHT, padx=30, pady=20)
        
        # Основна панель з кнопками
        main_frame = tk.Frame(self.root, bg=self.styles.COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Кнопки функцій вчителя - ПОВНИЙ НАБІР З ТЗ
        teacher_buttons = [
            ("👥 МОЇ КЛАСИ", self.app.show_teacher_classes, self.styles.COLORS['info']),
            ("📊 СТАТИСТИКА КЛАСУ", self.show_class_stats, self.styles.COLORS['warning']),
            ("➕ ВИСТАВИТИ ОЦІНКУ", self.app.show_add_grade, self.styles.COLORS['success']),
            ("🎁 НАГОРОДИТИ КЛАС", self.app.show_award_class, self.styles.COLORS['secondary']),
            ("🛒 МАГАЗИН ВЧИТЕЛЯ", self.app.show_teacher_shop_manager, self.styles.COLORS['primary']),
            ("📅 РОЗКЛАД", self.show_schedule, self.styles.COLORS['dark']),
            ("🚪 ВИЙТИ", self.app.logout, self.styles.COLORS['danger'])
        ]
        
        # Розміщення кнопок
        for i, (text, command, color) in enumerate(teacher_buttons):
            btn = tk.Button(main_frame,
                          text=text,
                          font=self.styles.FONTS['normal'],
                          bg=color,
                          fg='white',
                          height=3,
                          width=25,
                          command=command)
            btn.grid(row=i, column=0, padx=10, pady=10, sticky='nsew')
        
        # Налаштування розтягування
        main_frame.grid_rowconfigure(len(teacher_buttons), weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
    
    def show_class_stats(self):
        """Показати статистику класу"""
        from tkinter import messagebox
        messagebox.showinfo("Статистика", 
                          "Функція статистики класу у розробці.\n"
                          "Тут буде графіки успішності, середні бали тощо.")
    
    def show_schedule(self):
        """Показати розклад"""
        from tkinter import messagebox
        messagebox.showinfo("Розклад", 
                          "Функція розкладу у розробці.\n"
                          "Тут буде управління розкладом занять.")