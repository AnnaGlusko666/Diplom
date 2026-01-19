"""
Вікно вибору для вчителя
"""

import tkinter as tk
from tkinter import messagebox
from styles import AppStyles

class TeacherUI:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.styles = AppStyles
        
    def show_options(self):
        """Показати опції для вчителя"""
        # Очищення вікна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root,
                text="ВЧИТЕЛЬ",
                font=self.styles.FONTS['title'],
                fg=self.styles.COLORS['primary'],
                bg=self.styles.COLORS['background']).pack(pady=40)
        
        options_frame = tk.Frame(self.root, bg=self.styles.COLORS['background'])
        options_frame.pack(pady=30)
        
        # Кнопки вибору
        tk.Button(options_frame,
                 text="🔐 ВХІД У СИСТЕМУ",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['primary'],
                 fg='white',
                 width=25,
                 height=2,
                 command=self.show_login).pack(pady=10)
        
        tk.Button(options_frame,
                 text="📝 РЕЄСТРАЦІЯ ВЧИТЕЛЯ",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['info'],
                 fg='white',
                 width=25,
                 height=2,
                 command=self.show_register).pack(pady=10)
        
        tk.Button(options_frame,
                 text="➕ СТВОРИТИ КЛАС",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['success'],
                 fg='white',
                 width=25,
                 height=2,
                 command=self.app.show_create_class).pack(pady=10)
        
        # Кнопка назад
        tk.Button(self.root,
                 text="НАЗАД",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['secondary'],
                 fg='white',
                 width=15,
                 command=self.app.show_main_menu).pack(pady=30)
    
    def show_login(self):
        """Показати вікно входу для вчителя"""
        # Очищення вікна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root,
                text="ВХІД ВЧИТЕЛЯ",
                font=self.styles.FONTS['title'],
                fg=self.styles.COLORS['primary'],
                bg=self.styles.COLORS['background']).pack(pady=40)
        
        form_frame = tk.Frame(self.root, bg=self.styles.COLORS['background'])
        form_frame.pack(pady=20)
        
        # Логін
        tk.Label(form_frame,
                text="Логін:",
                font=self.styles.FONTS['normal'],
                bg=self.styles.COLORS['background']).grid(row=0, column=0, pady=10, padx=10, sticky='e')
        
        self.login_entry = tk.Entry(form_frame, font=self.styles.FONTS['normal'], width=30)
        self.login_entry.grid(row=0, column=1, pady=10, padx=10)
        self.login_entry.insert(0, 'admin')  # Тестовий логін
        
        # Пароль
        tk.Label(form_frame,
                text="Пароль:",
                font=self.styles.FONTS['normal'],
                bg=self.styles.COLORS['background']).grid(row=1, column=0, pady=10, padx=10, sticky='e')
        
        self.password_entry = tk.Entry(form_frame, font=self.styles.FONTS['normal'], width=30, show='*')
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)
        self.password_entry.insert(0, 'admin123')  # Тестовий пароль
        
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
                 command=self.show_options).pack(side=tk.LEFT, padx=10)
    
    def show_register(self):
        """Показати вікно реєстрації вчителя"""
        # Очищення вікна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root,
                text="РЕЄСТРАЦІЯ ВЧИТЕЛЯ",
                font=self.styles.FONTS['title'],
                fg=self.styles.COLORS['primary'],
                bg=self.styles.COLORS['background']).pack(pady=30)
        
        form_frame = tk.Frame(self.root, bg=self.styles.COLORS['background'])
        form_frame.pack(pady=20)
        
        # Поля форми
        fields = [
            ("Повне ім'я:", "full_name"),
            ("Логін:", "username"),
            ("Пароль:", "password", True)
        ]
        
        self.entries = {}
        
        for i, field in enumerate(fields):
            label_text = field[0]
            field_name = field[1]
            is_password = len(field) > 2 and field[2]
            
            tk.Label(form_frame,
                    text=label_text,
                    font=self.styles.FONTS['normal'],
                    bg=self.styles.COLORS['background']).grid(row=i, column=0, pady=10, padx=10, sticky='e')
            
            entry = tk.Entry(form_frame, font=self.styles.FONTS['normal'], width=30)
            if is_password:
                entry.config(show='*')
            entry.grid(row=i, column=1, pady=10, padx=10)
            
            self.entries[field_name] = entry
        
        button_frame = tk.Frame(self.root, bg=self.styles.COLORS['background'])
        button_frame.pack(pady=30)
        
        tk.Button(button_frame,
                 text="ЗАРЕЄСТРУВАТИ",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['success'],
                 fg='white',
                 width=20,
                 command=self.register).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame,
                 text="НАЗАД",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['secondary'],
                 fg='white',
                 width=15,
                 command=self.show_options).pack(side=tk.LEFT, padx=10)
    
    def login(self):
        """Виконати вхід вчителя"""
        username = self.login_entry.get()
        password = self.password_entry.get()
        
        user = self.app.auth.login(username, password, "teacher")
        
        if user:
            self.app.current_user = user
            self.app.show_teacher_dashboard()
        else:
            messagebox.showerror("Помилка", "Невірний логін або пароль!")
    
    def register(self):
        """Зареєструвати нового вчителя"""
        full_name = self.entries['full_name'].get()
        username = self.entries['username'].get()
        password = self.entries['password'].get()
        
        if not all([full_name, username, password]):
            messagebox.showerror("Помилка", "Будь ласка, заповніть всі поля")
            return
        
        teacher = self.app.auth.register_teacher(full_name, username, password)
        
        if teacher:
            messagebox.showinfo("Успіх", f"Вчителя {full_name} успішно зареєстровано!\nЛогін: {username}")
            self.show_options()