"""
Вікно генерації акаунтів учнів
"""

import tkinter as tk
from tkinter import messagebox
import random
import string
from styles import AppStyles

class GenerateStudentsUI:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.styles = AppStyles
        self.class_id = None
        
    def show(self, class_id):
        """Показати вікно генерації учнів"""
        self.class_id = class_id
        
        # Очищення вікна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root,
                text="ГЕНЕРАЦІЯ АКАУНТІВ УЧНІВ",
                font=self.styles.FONTS['title'],
                fg=self.styles.COLORS['primary'],
                bg=self.styles.COLORS['background']).pack(pady=20)
        
        # Інструкція
        tk.Label(self.root,
                text="Введіть імена учнів (кожне з нового рядка):",
                font=self.styles.FONTS['normal'],
                bg=self.styles.COLORS['background']).pack(pady=10)
        
        # Текстове поле для імен
        text_frame = tk.Frame(self.root, bg=self.styles.COLORS['background'])
        text_frame.pack(pady=10, padx=50, fill=tk.BOTH, expand=True)
        
        self.text_widget = tk.Text(text_frame, height=10, width=50, font=('Arial', 11))
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=scrollbar.set)
        
        # Приклад даних
        example_names = "Іваненко Петро\nКоваленко Марія\nСидоренко Олександр\nШевченко Анна"
        self.text_widget.insert('1.0', example_names)
        
        button_frame = tk.Frame(self.root, bg=self.styles.COLORS['background'])
        button_frame.pack(pady=20)
        
        tk.Button(button_frame,
                 text="ЗГЕНЕРУВАТИ",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['success'],
                 fg='white',
                 width=20,
                 command=self.generate_accounts).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame,
                 text="НАЗАД",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['secondary'],
                 fg='white',
                 width=15,
                 command=self.app.show_teacher_options).pack(side=tk.LEFT, padx=10)
    
    def generate_accounts(self):
        """Згенерувати акаунти учнів"""
        names_text = self.text_widget.get('1.0', tk.END).strip()
        if not names_text:
            messagebox.showerror("Помилка", "Будь ласка, введіть імена учнів")
            return
        
        names = [name.strip() for name in names_text.split('\n') if name.strip()]
        
        # Генерація логінів та паролів
        results = []
        class_info = self.app.db.get_class_by_id(self.class_id)
        
        for name in names:
            # Генерація логіна
            name_parts = name.split()
            if len(name_parts) >= 2:
                first_letter = name_parts[0][0].lower()
                last_name = name_parts[-1].lower()
                username = f"{first_letter}{last_name}10"
            else:
                username = name.lower().replace(' ', '') + "10"
            
            # Генерація пароля
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            
            results.append(f"{name}: логін={username}, пароль={password}")
        
        # Показати результати
        self.show_results(results, len(names))
    
    def show_results(self, results, count):
        """Показати результати генерації"""
        result_window = tk.Toplevel(self.root)
        result_window.title("Створені акаунти")
        result_window.geometry("500x400")
        result_window.configure(bg=self.styles.COLORS['background'])
        
        tk.Label(result_window,
                text="Створені акаунти учнів:",
                font=self.styles.FONTS['header'],
                bg=self.styles.COLORS['background']).pack(pady=10)
        
        result_text = tk.Text(result_window, height=15, width=60, font=('Arial', 10))
        result_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        for result in results:
            result_text.insert(tk.END, result + '\n')
        
        result_text.config(state=tk.DISABLED)
        
        tk.Button(result_window,
                 text="Закрити",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['primary'],
                 fg='white',
                 command=result_window.destroy).pack(pady=10)
        
        messagebox.showinfo("Успіх", f"Створено {count} акаунтів учнів")
        self.app.show_teacher_options()