"""
Модуль для нагородження всього класу монетами
"""

import tkinter as tk
from tkinter import messagebox
from motivation import MotivationSystem
from styles import AppStyles

class AwardClassUI:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.styles = AppStyles
        self.motivation = MotivationSystem(app_instance.db)
        
    def show(self):
        """Показати вікно нагородження класу"""
        self.award_window = tk.Toplevel(self.root)
        self.award_window.title("Нагородження класу")
        self.award_window.geometry("500x400")
        self.award_window.configure(bg=self.styles.COLORS['background'])
        
        tk.Label(self.award_window,
                text="🎁 НАГОРОДЖЕННЯ КЛАСУ",
                font=self.styles.FONTS['title'],
                fg=self.styles.COLORS['primary'],
                bg=self.styles.COLORS['background']).pack(pady=20)
        
        # Отримуємо класи вчителя
        classes = self.app.db.get_teacher_classes(self.app.current_user.id)
        
        if not classes:
            tk.Label(self.award_window,
                    text="У вас немає класів",
                    font=self.styles.FONTS['normal'],
                    fg=self.styles.COLORS['secondary'],
                    bg=self.styles.COLORS['background']).pack(pady=50)
            return
        
        # Вибор класу
        tk.Label(self.award_window,
                text="Оберіть клас для нагородження:",
                font=self.styles.FONTS['normal'],
                bg=self.styles.COLORS['background']).pack(pady=10)
        
        self.class_var = tk.StringVar()
        
        for i, class_obj in enumerate(classes):
            class_frame = tk.Frame(self.award_window, bg=self.styles.COLORS['background'])
            class_frame.pack(pady=5)
            
            rb = tk.Radiobutton(class_frame,
                              text=f"Клас {class_obj.name}",
                              variable=self.class_var,
                              value=class_obj.id,
                              font=self.styles.FONTS['normal'],
                              bg=self.styles.COLORS['background'])
            rb.pack(side=tk.LEFT)
            
            # Кількість учнів
            students_count = len(class_obj.student_ids)
            tk.Label(class_frame,
                    text=f"({students_count} учнів)",
                    font=self.styles.FONTS['small'],
                    fg=self.styles.COLORS['secondary'],
                    bg=self.styles.COLORS['background']).pack(side=tk.LEFT, padx=10)
        
        if classes:
            self.class_var.set(classes[0].id)
        
        # Кількість монет
        tk.Label(self.award_window,
                text="Кількість монет для кожного учня:",
                font=self.styles.FONTS['normal'],
                bg=self.styles.COLORS['background']).pack(pady=10)
        
        self.coins_var = tk.StringVar(value="10")
        coins_entry = tk.Entry(self.award_window,
                              textvariable=self.coins_var,
                              width=10,
                              font=self.styles.FONTS['normal'])
        coins_entry.pack(pady=5)
        
        # Причина
        tk.Label(self.award_window,
                text="Причина нагородження:",
                font=self.styles.FONTS['normal'],
                bg=self.styles.COLORS['background']).pack(pady=10)
        
        self.reason_text = tk.Text(self.award_window, height=3, width=40)
        self.reason_text.pack(pady=5)
        self.reason_text.insert("1.0", "За активну роботу на уроці")
        
        # Кнопка нагородження
        tk.Button(self.award_window,
                 text="НАГОРОДИТИ КЛАС",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['success'],
                 fg='white',
                 command=self.award_class).pack(pady=20)
    
    def award_class(self):
        """Нагородити клас монетами"""
        try:
            class_id = self.class_var.get()
            coins = int(self.coins_var.get())
            reason = self.reason_text.get("1.0", tk.END).strip()
            
            if not class_id:
                messagebox.showerror("Помилка", "Оберіть клас")
                return
            
            if coins <= 0:
                messagebox.showerror("Помилка", "Кількість монет має бути більше 0")
                return
            
            if not reason:
                messagebox.showerror("Помилка", "Введіть причину нагородження")
                return
            
            # Нагороджуємо клас
            results = self.motivation.award_coins_to_class(
                class_id=class_id,
                teacher_id=self.app.current_user.id,
                coins=coins,
                reason=reason
            )
            
            messagebox.showinfo("Успіх", 
                              f"Клас успішно нагороджений!\n"
                              f"Кожен учень отримав {coins} монет\n"
                              f"Загальна кількість учнів: {len(results)}")
            self.award_window.destroy()
            
        except ValueError:
            messagebox.showerror("Помилка", "Будь ласка, введіть коректну кількість монет")