"""
Панель управління для учня
"""

import tkinter as tk
from styles import AppStyles

class StudentDashboard:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.styles = AppStyles
        
    def show(self):
        """Показати панель учня"""
        # Очищення вікна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Профіль учня
        profile = self.app.db.get_student_profile(self.app.current_user.id)
        
        # Верхня панель
        header_frame = tk.Frame(self.root, bg=self.styles.COLORS['primary'], height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame,
                text=f"👤 {self.app.current_user.full_name}",
                font=('Arial', 20, 'bold'),
                fg='white',
                bg=self.styles.COLORS['primary']).pack(side=tk.LEFT, padx=30, pady=20)
        
        # Інформація про монети та бали
        stats_frame = tk.Frame(header_frame, bg=self.styles.COLORS['primary'])
        stats_frame.pack(side=tk.RIGHT, padx=30, pady=20)
        
        tk.Label(stats_frame,
                text=f"💰 {profile.coins} монет",
                font=('Arial', 14, 'bold'),
                fg='white',
                bg=self.styles.COLORS['primary']).pack(side=tk.LEFT, padx=10)
        
        tk.Label(stats_frame,
                text=f"🏅 {len(profile.badges)} відзнак",
                font=('Arial', 14, 'bold'),
                fg='white',
                bg=self.styles.COLORS['primary']).pack(side=tk.LEFT, padx=10)
        
        tk.Label(stats_frame,
                text=f"📊 {profile.average_grade:.1f} середній бал",
                font=('Arial', 14, 'bold'),
                fg='white',
                bg=self.styles.COLORS['primary']).pack(side=tk.LEFT, padx=10)
        
        # Основна панель з кнопками
        main_frame = tk.Frame(self.root, bg=self.styles.COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Кнопки функцій
        buttons = [
            ("📚 МОЇ ОЦІНКИ", self.app.show_student_grades, self.styles.COLORS['info']),
            ("🏅 ВІДЗНАКИ", self.app.show_student_badges, self.styles.COLORS['warning']),
            ("🛒 МАГАЗИН", self.app.show_student_shop, self.styles.COLORS['success']),
            ("👤 ПРОФІЛЬ", self.app.show_student_profile, self.styles.COLORS['secondary']),
            ("🔐 ЗМІНИТИ ПАРОЛЬ", self.app.change_password, self.styles.COLORS['dark']),
            ("🚪 ВИЙТИ", self.app.logout, self.styles.COLORS['danger'])
        ]
        
        # Розміщення кнопок в сітці
        for i, (text, command, color) in enumerate(buttons):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(main_frame,
                          text=text,
                          font=('Arial', 12, 'bold'),
                          bg=color,
                          fg='white',
                          height=3,
                          width=20,
                          command=command)
            btn.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Налаштування розтягування сітки
        for i in range(2):
            main_frame.grid_columnconfigure(i, weight=1)
        for i in range((len(buttons) + 1) // 2):
            main_frame.grid_rowconfigure(i, weight=1)