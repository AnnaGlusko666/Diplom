"""
Вікно магазину для учня
"""

import tkinter as tk
from tkinter import messagebox
from styles import AppStyles

class StudentShopUI:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.styles = AppStyles
        
    def show(self):
        """Показати магазин"""
        shop_items = self.app.db.get_shop_items()
        profile = self.app.db.get_student_profile(self.app.current_user.id)
        
        self.shop_window = tk.Toplevel(self.root)
        self.shop_window.title("Магазин")
        self.shop_window.geometry("800x600")
        self.shop_window.configure(bg=self.styles.COLORS['background'])
        
        # Заголовок та баланс
        header_frame = tk.Frame(self.shop_window, bg=self.styles.COLORS['primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_frame,
                text="🛒 МАГАЗИН",
                font=self.styles.FONTS['title'],
                fg='white',
                bg=self.styles.COLORS['primary']).pack(side=tk.LEFT, padx=30, pady=15)
        
        tk.Label(header_frame,
                text=f"💰 {profile.coins} монет",
                font=self.styles.FONTS['header'],
                fg='white',
                bg=self.styles.COLORS['primary']).pack(side=tk.RIGHT, padx=30, pady=15)
        
        # Сітка товарів
        self.create_shop_items(shop_items, profile)
    
    def create_shop_items(self, shop_items, profile):
        """Створити відображення товарів"""
        canvas = tk.Canvas(self.shop_window, bg=self.styles.COLORS['background'])
        scrollbar = tk.Scrollbar(self.shop_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.styles.COLORS['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        if not shop_items:
            tk.Label(scrollable_frame,
                    text="Наразі в магазині немає товарів",
                    font=self.styles.FONTS['normal'],
                    fg=self.styles.COLORS['secondary'],
                    bg=self.styles.COLORS['background']).pack(pady=50)
        else:
            # Розміщення товарів в сітці 2x2
            for i, item in enumerate(shop_items):
                row = i // 2
                col = i % 2
                
                is_bought = item.id in profile.bought_items
                can_afford = profile.coins >= item.price
                
                self.create_item_card(scrollable_frame, row, col, item, is_bought, can_afford)
        
        # Налаштування сітки
        scrollable_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(1, weight=1)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")
    
    def create_item_card(self, parent, row, col, item, is_bought, can_afford):
        """Створити картку товару"""
        # Фрейм товару
        item_frame = tk.Frame(parent,
                             bg=self.styles.COLORS['light'],
                             relief=tk.RAISED,
                             borderwidth=2)
        item_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
        
        # Категорія
        category_icons = {
            'avatar': '👤',
            'privilege': '⭐',
            'profile_item': '🎁'
        }
        icon = category_icons.get(item.category, '📦')
        
        tk.Label(item_frame,
                text=f"{icon} {item.name}",
                font=self.styles.FONTS['header'],
                bg=self.styles.COLORS['light']).pack(pady=(10, 5))
        
        # Опис
        tk.Label(item_frame,
                text=item.description,
                font=self.styles.FONTS['small'],
                bg=self.styles.COLORS['light'],
                wraplength=300).pack(pady=5, padx=10)
        
        # Ціна
        price_color = self.styles.COLORS['success'] if can_afford else self.styles.COLORS['danger']
        tk.Label(item_frame,
                text=f"Ціна: {item.price} монет",
                font=('Arial', 12, 'bold'),
                fg=price_color,
                bg=self.styles.COLORS['light']).pack(pady=5)
        
        # Кнопка покупки
        if is_bought:
            status_label = tk.Label(item_frame,
                                  text="✓ ВЖЕ КУПЛЕНО",
                                  font=('Arial', 10, 'bold'),
                                  fg=self.styles.COLORS['success'],
                                  bg=self.styles.COLORS['light'])
            status_label.pack(pady=10)
        else:
            def buy_item():
                if self.app.db.get_student_profile(self.app.current_user.id).coins < item.price:
                    messagebox.showerror("Помилка", "Недостатньо монет!")
                    return
                
                if messagebox.askyesno("Підтвердження", 
                                      f"Купити '{item.name}' за {item.price} монет?"):
                    if self.app.db.purchase_item(self.app.current_user.id, item.id, item.price):
                        messagebox.showinfo("Успіх", "Товар успішно куплено!")
                        self.shop_window.destroy()
                        self.app.show_student_shop()
                    else:
                        messagebox.showerror("Помилка", "Не вдалося купити товар")
            
            buy_btn = tk.Button(item_frame,
                              text="КУПИТИ",
                              font=('Arial', 11, 'bold'),
                              bg=self.styles.COLORS['primary'] if can_afford else self.styles.COLORS['secondary'],
                              fg='white',
                              state=tk.NORMAL if can_afford else tk.DISABLED,
                              command=buy_item)
            buy_btn.pack(pady=10)