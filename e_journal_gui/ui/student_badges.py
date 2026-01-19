"""
Вікно перегляду відзнак учня
"""

import tkinter as tk
from styles import AppStyles

class StudentBadgesUI:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.styles = AppStyles
        
    def show(self):
        """Показати відзнаки учня"""
        all_badges = self.app.db.get_all_badges()
        profile = self.app.db.get_student_profile(self.app.current_user.id)
        student_badges = profile.badges
        
        self.badges_window = tk.Toplevel(self.root)
        self.badges_window.title("Мої відзнаки")
        self.badges_window.geometry("700x500")
        self.badges_window.configure(bg=self.styles.COLORS['background'])
        
        tk.Label(self.badges_window,
                text="МОЇ ВІДЗНАКИ",
                font=self.styles.FONTS['title'],
                fg=self.styles.COLORS['primary'],
                bg=self.styles.COLORS['background']).pack(pady=20)
        
        tk.Label(self.badges_window,
                text=f"🏅 {len(student_badges)} з {len(all_badges)} відзнак",
                font=self.styles.FONTS['normal'],
                fg=self.styles.COLORS['secondary'],
                bg=self.styles.COLORS['background']).pack()
        
        # Сітка для відзнак
        self.create_badges_display(all_badges, student_badges)
    
    def create_badges_display(self, all_badges, student_badges):
        """Створити відображення відзнак"""
        canvas = tk.Canvas(self.badges_window, bg=self.styles.COLORS['background'])
        scrollbar = tk.Scrollbar(self.badges_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.styles.COLORS['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        row = 0
        for badge in all_badges:
            has_badge = badge.id in student_badges
            
            # Визначення кольору за рідкістю
            if badge.rarity.value == 'common':
                color = self.styles.COLORS['secondary']
                icon = "🥉"
            elif badge.rarity.value == 'rare':
                color = self.styles.COLORS['info']
                icon = "🥈"
            elif badge.rarity.value == 'epic':
                color = self.styles.COLORS['primary']
                icon = "🥇"
            else:
                color = self.styles.COLORS['warning']
                icon = "🏆"
            
            # Фрейм для відзнаки
            badge_frame = tk.Frame(scrollable_frame, 
                                  bg=color if has_badge else self.styles.COLORS['light'],
                                  relief=tk.RIDGE,
                                  borderwidth=1)
            badge_frame.grid(row=row, column=0, sticky='ew', padx=20, pady=5)
            row += 1
            
            # Іконка та назва
            icon_label = tk.Label(badge_frame,
                                 text=icon,
                                 font=('Arial', 20),
                                 bg=color if has_badge else self.styles.COLORS['light'])
            icon_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10)
            
            # Назва
            name_label = tk.Label(badge_frame,
                                 text=badge.name,
                                 font=('Arial', 12, 'bold'),
                                 bg=color if has_badge else self.styles.COLORS['light'],
                                 fg='white' if has_badge else self.styles.COLORS['dark'])
            name_label.grid(row=0, column=1, sticky='w', padx=5, pady=(10, 0))
            
            # Опис
            desc_label = tk.Label(badge_frame,
                                 text=badge.description,
                                 font=('Arial', 10),
                                 bg=color if has_badge else self.styles.COLORS['light'],
                                 fg='white' if has_badge else self.styles.COLORS['secondary'])
            desc_label.grid(row=1, column=1, sticky='w', padx=5, pady=(0, 10))
            
            # Статус
            status_text = "✓ Отримано" if has_badge else "✗ Ще не отримано"
            status_color = 'white' if has_badge else self.styles.COLORS['danger']
            
            status_label = tk.Label(badge_frame,
                                   text=status_text,
                                   font=('Arial', 10, 'bold'),
                                   bg=color if has_badge else self.styles.COLORS['light'],
                                   fg=status_color)
            status_label.grid(row=0, column=2, rowspan=2, padx=20, pady=10)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")