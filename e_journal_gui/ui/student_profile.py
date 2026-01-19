"""
Вікно профілю учня
"""

import tkinter as tk
from styles import AppStyles

class StudentProfileUI:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.styles = AppStyles
        
    def show(self):
        """Показати профіль учня"""
        profile = self.app.db.get_student_profile(self.app.current_user.id)
        
        self.profile_window = tk.Toplevel(self.root)
        self.profile_window.title("Мій профіль")
        self.profile_window.geometry("600x500")
        self.profile_window.configure(bg=self.styles.COLORS['background'])
        
        # Заголовок
        tk.Label(self.profile_window,
                text="👤 МІЙ ПРОФІЛЬ",
                font=self.styles.FONTS['title'],
                fg=self.styles.COLORS['primary'],
                bg=self.styles.COLORS['background']).pack(pady=20)
        
        # Особиста інформація
        self.create_personal_info()
        
        # Статистика
        self.create_statistics(profile)
        
        # Куплені товари
        self.create_purchased_items(profile)
        
        # Кнопка закриття
        tk.Button(self.profile_window,
                 text="Закрити",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['primary'],
                 fg='white',
                 width=15,
                 command=self.profile_window.destroy).pack(pady=20)
    
    def create_personal_info(self):
        """Створити розділ з особистою інформацією"""
        info_frame = tk.Frame(self.profile_window, 
                             bg=self.styles.COLORS['light'], 
                             relief=tk.RIDGE, 
                             borderwidth=2)
        info_frame.pack(fill=tk.X, padx=50, pady=10)
        
        tk.Label(info_frame,
                text="📋 Особиста інформація",
                font=self.styles.FONTS['header'],
                bg=self.styles.COLORS['light']).pack(pady=10)
        
        info_text = f"""
        Ім'я: {self.app.current_user.full_name}
        Логін: {self.app.current_user.username}
        Клас: {self.app.current_user.class_id if self.app.current_user.class_id else "Не призначено"}
        Аватар: {self.app.current_user.avatar}
        """
        
        tk.Label(info_frame,
                text=info_text,
                font=self.styles.FONTS['small'],
                bg=self.styles.COLORS['light'],
                justify=tk.LEFT).pack(pady=10, padx=20)
    
    def create_statistics(self, profile):
        """Створити розділ зі статистикою"""
        stats_frame = tk.Frame(self.profile_window, 
                              bg=self.styles.COLORS['light'], 
                              relief=tk.RIDGE, 
                              borderwidth=2)
        stats_frame.pack(fill=tk.X, padx=50, pady=10)
        
        tk.Label(stats_frame,
                text="📊 Статистика",
                font=self.styles.FONTS['header'],
                bg=self.styles.COLORS['light']).pack(pady=10)
        
        stats_text = f"""
        Монети: {profile.coins}
        Відзнаки: {len(profile.badges)}
        Оцінок: {profile.total_grades}
        Середній бал: {profile.average_grade:.1f}
        """
        
        tk.Label(stats_frame,
                text=stats_text,
                font=self.styles.FONTS['small'],
                bg=self.styles.COLORS['light'],
                justify=tk.LEFT).pack(pady=10, padx=20)
    
    def create_purchased_items(self, profile):
        """Створити розділ з купленими товарами"""
        bought_frame = tk.Frame(self.profile_window, 
                               bg=self.styles.COLORS['light'], 
                               relief=tk.RIDGE, 
                               borderwidth=2)
        bought_frame.pack(fill=tk.X, padx=50, pady=10)
        
        tk.Label(bought_frame,
                text="🛍️ Куплені товари",
                font=self.styles.FONTS['header'],
                bg=self.styles.COLORS['light']).pack(pady=10)
        
        if profile.bought_items:
            shop_items = self.app.db.get_shop_items()
            bought_names = []
            for item_id in profile.bought_items:
                for item in shop_items:
                    if item.id == item_id:
                        bought_names.append(item.name)
                        break
            
            for name in bought_names:
                tk.Label(bought_frame,
                        text=f"• {name}",
                        font=self.styles.FONTS['small'],
                        bg=self.styles.COLORS['light']).pack(anchor='w', padx=30, pady=2)
        else:
            tk.Label(bought_frame,
                    text="Немає куплених товарів",
                    font=('Arial', 11, 'italic'),
                    fg=self.styles.COLORS['secondary'],
                    bg=self.styles.COLORS['light']).pack(pady=10)