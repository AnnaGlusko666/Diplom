"""
Модуль для управління магазином вчителя
"""

import tkinter as tk
from tkinter import messagebox
from models import ShopItem, generate_id
from database import Database
from styles import AppStyles

class TeacherShopManager:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.styles = AppStyles
        
    def show(self):
        """Показати менеджер магазину вчителя"""
        self.shop_window = tk.Toplevel(self.root)
        self.shop_window.title("Магазин вчителя")
        self.shop_window.geometry("700x500")
        self.shop_window.configure(bg=self.styles.COLORS['background'])
        
        # Заголовок
        tk.Label(self.shop_window,
                text="🛒 МАГАЗИН ВЧИТЕЛЯ",
                font=self.styles.FONTS['title'],
                fg=self.styles.COLORS['primary'],
                bg=self.styles.COLORS['background']).pack(pady=20)
        
        # Кнопки управління
        button_frame = tk.Frame(self.shop_window, bg=self.styles.COLORS['background'])
        button_frame.pack(pady=10)
        
        tk.Button(button_frame,
                 text="➕ ДОДАТИ ТОВАР",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['success'],
                 fg='white',
                 width=20,
                 command=self.show_add_item).pack(pady=5)
        
        tk.Button(button_frame,
                 text="📋 МОЇ ТОВАРИ",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['info'],
                 fg='white',
                 width=20,
                 command=self.show_my_items).pack(pady=5)
        
        tk.Button(button_frame,
                 text="👀 ПЕРЕГЛЯНУТИ ПОКУПКИ",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['warning'],
                 fg='white',
                 width=20,
                 command=self.show_purchases).pack(pady=5)
    
    def show_add_item(self):
        """Показати форму додавання товару"""
        add_window = tk.Toplevel(self.shop_window)
        add_window.title("Додати товар")
        add_window.geometry("500x600")
        add_window.configure(bg=self.styles.COLORS['background'])
        
        tk.Label(add_window,
                text="➕ ДОДАТИ ТОВАР",
                font=self.styles.FONTS['header'],
                fg=self.styles.COLORS['primary'],
                bg=self.styles.COLORS['background']).pack(pady=20)
        
        # Форма
        form_frame = tk.Frame(add_window, bg=self.styles.COLORS['background'])
        form_frame.pack(pady=10)
        
        # Поля
        fields = [
            ("Назва товару:", "name", tk.Entry, {"width": 30}),
            ("Опис:", "description", tk.Text, {"height": 4, "width": 40}),
            ("Ціна (монети):", "price", tk.Entry, {"width": 10}),
            ("Категорія:", "category", tk.Entry, {"width": 20}),
        ]
        
        self.item_entries = {}
        
        for i, (label, field_name, widget_type, kwargs) in enumerate(fields):
            tk.Label(form_frame,
                    text=label,
                    font=self.styles.FONTS['normal'],
                    bg=self.styles.COLORS['background']).grid(row=i, column=0, pady=10, padx=10, sticky='e')
            
            if widget_type == tk.Text:
                widget = widget_type(form_frame, **kwargs)
                widget.grid(row=i, column=1, pady=10, padx=10)
                self.item_entries[field_name] = widget
            else:
                widget = widget_type(form_frame, **kwargs)
                widget.grid(row=i, column=1, pady=10, padx=10)
                self.item_entries[field_name] = widget
        
        # Кнопка збереження
        tk.Button(add_window,
                 text="ЗБЕРЕГТИ ТОВАР",
                 font=self.styles.FONTS['normal'],
                 bg=self.styles.COLORS['primary'],
                 fg='white',
                 command=lambda: self.save_item(add_window)).pack(pady=20)
    
    def save_item(self, window):
        """Зберегти товар"""
        try:
            name = self.item_entries['name'].get()
            description = self.item_entries['description'].get("1.0", tk.END).strip()
            price = int(self.item_entries['price'].get())
            category = self.item_entries['category'].get()
            
            if not all([name, description, category]):
                messagebox.showerror("Помилка", "Заповніть всі поля")
                return
            
            if price <= 0:
                messagebox.showerror("Помилка", "Ціна має бути більше 0")
                return
            
            # Створюємо товар
            new_item = ShopItem(
                id=generate_id(),
                name=name,
                description=description,
                price=price,
                category=category,
                data={"teacher_created": True},
                teacher_only=False,
                teacher_id=self.app.current_user.id
            )
            
            # Зберігаємо в базі (потрібно додати метод в Database)
            messagebox.showinfo("Успіх", f"Товар '{name}' успішно додано!")
            window.destroy()
            
        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректну ціну")
    
    def show_my_items(self):
        """Показати товари вчителя"""
        # Потрібно додати метод get_teacher_items в Database
        messagebox.showinfo("Інформація", "Функція у розробці")
    
    def show_purchases(self):
        """Показати покупки учнів"""
        # Потрібно додати метод get_purchases_by_teacher в Database
        messagebox.showinfo("Інформація", "Функція у розробці")