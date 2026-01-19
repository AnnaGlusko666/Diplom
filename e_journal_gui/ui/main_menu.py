"""
Головне меню програми
"""

import tkinter as tk
from styles import AppStyles

class MainMenu:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.styles = AppStyles
        
    def show(self):
        """Показати головне меню"""
        # Очищення вікна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Заголовок
        title_frame = tk.Frame(self.root, bg=self.styles.COLORS['background'])
        title_frame.pack(pady=50)
        
        tk.Label(title_frame, 
                text="ЕЛЕКТРОННИЙ ЖУРНАЛ",
                font=self.styles.FONTS['title'],
                fg=self.styles.COLORS['primary'],
                bg=self.styles.COLORS['background']).pack()
        
        tk.Label(title_frame,
                text="Система мотивації для учнів",
                font=self.styles.FONTS['header'],
                fg=self.styles.COLORS['secondary'],
                bg=self.styles.COLORS['background']).pack(pady=10)
        
        # Кнопки вибору
        button_frame = tk.Frame(self.root, bg=self.styles.COLORS['background'])
        button_frame.pack(pady=50)
        
        # Кнопка для учня
        student_btn = tk.Button(button_frame,
                              text="👤 УЧЕНЬ",
                              font=('Arial', 14, 'bold'),
                              bg=self.styles.COLORS['primary'],
                              fg='white',
                              width=20,
                              height=3,
                              command=self.app.show_student_login,
                              relief=tk.RAISED,
                              borderwidth=3)
        student_btn.pack(pady=10)
        
        # Кнопка для вчителя
        teacher_btn = tk.Button(button_frame,
                               text="👨‍🏫 ВЧИТЕЛЬ",
                               font=('Arial', 14, 'bold'),
                               bg=self.styles.COLORS['success'],
                               fg='white',
                               width=20,
                               height=3,
                               command=self.app.show_teacher_options,
                               relief=tk.RAISED,
                               borderwidth=3)
        teacher_btn.pack(pady=10)
        
        # Інформація про тестові дані
        info_frame = tk.Frame(self.root, bg=self.styles.COLORS['background'])
        info_frame.pack(pady=20)
        
        tk.Label(info_frame,
                text="Тестові дані для входу:",
                font=self.styles.FONTS['small'],
                fg=self.styles.COLORS['dark'],
                bg=self.styles.COLORS['background']).pack()
        
        tk.Label(info_frame,
                text="Вчитель: логін=admin, пароль=admin123",
                font=('Arial', 10, 'italic'),
                fg=self.styles.COLORS['secondary'],
                bg=self.styles.COLORS['background']).pack()