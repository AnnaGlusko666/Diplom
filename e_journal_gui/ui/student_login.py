"""
Вікно входу для учня
"""

import tkinter as tk
from tkinter import messagebox
from styles import AppStyles

class StudentLogin:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.styles = AppStyles
        
    def show(self):
        """Показати вікно входу для учня"""
        # Очищення вікна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Заголовок
        tk.Label(self.root,
                text="ВХІД УЧНЯ",
                font=self.styles.FONTS['title'],
                fg=self.styles.COLORS['primary'],
                bg=self.styles.COLORS['background']).pack(pady=40)
        
        # Форма входу
        form_frame = tk.Frame(self.root, bg=self.styles.COLORS['background'])
        form_frame.pack(pady=20)
        
        # Логін
        tk.Label(form_frame,
                text="Логін:",
                font=self.styles.FONTS['normal'],
                bg=self.styles.COLORS['background']).grid(row=0, column=0, pady=10, padx=10, sticky='e')
        
        self.login_entry = tk.Entry(form_frame, font=self.styles.FONTS['normal'], width=30)
        self.login_entry.grid(row=0, column=1, pady=10, padx=10)
        self.login_entry.focus()
        
        # Пароль
        tk.Label(form_frame,
                text="Пароль:",
                font=self.styles.FONTS['normal'],
                bg=self.styles.COLORS['background']).grid(row=1, column=0, pady=10, padx=10, sticky='e')
        
        self.password_entry = tk.Entry(form_frame, font=self.styles.FONTS['normal'], width=30, show='*')
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Кнопки
        button_frame = tk.Frame(self.root, bg=self.styles.COLORS['background'])
        button_frame.pack(pady=30)
        
        tk.Button(button_frame,
                 text="УВІЙТИ",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['primary'],
                 fg='white',
                 width=15,
                 command=self.login).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame,
                 text="НАЗАД",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['secondary'],
                 fg='white',
                 width=15,
                 command=self.app.show_main_menu).pack(side=tk.LEFT, padx=10)
    
    def login(self):
        """Виконати вхід"""
        username = self.login_entry.get()
        password = self.password_entry.get()
        
        user = self.app.auth.login(username, password, "student")
        
        if user:
            self.app.current_user = user
            self.app.show_student_dashboard()
        else:
            messagebox.showerror("Помилка", "Невірний логін або пароль!")