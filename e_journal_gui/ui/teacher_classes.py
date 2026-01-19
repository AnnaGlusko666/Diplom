"""
Вікно перегляду класів вчителя
"""

import tkinter as tk
from styles import AppStyles

class TeacherClassesUI:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.styles = AppStyles
        
    def show(self):
        """Показати класи вчителя"""
        classes = self.app.db.get_teacher_classes(self.app.current_user.id)
        
        self.classes_window = tk.Toplevel(self.root)
        self.classes_window.title("Мої класи")
        self.classes_window.geometry("600x400")
        self.classes_window.configure(bg=self.styles.COLORS['background'])
        
        tk.Label(self.classes_window,
                text="МОЇ КЛАСИ",
                font=self.styles.FONTS['title'],
                fg=self.styles.COLORS['primary'],
                bg=self.styles.COLORS['background']).pack(pady=20)
        
        if not classes:
            tk.Label(self.classes_window,
                    text="У вас ще немає класів",
                    font=self.styles.FONTS['normal'],
                    fg=self.styles.COLORS['secondary'],
                    bg=self.styles.COLORS['background']).pack(pady=50)
        else:
            # Список класів
            self.create_classes_list(classes)
    
    def create_classes_list(self, classes):
        """Створити список класів"""
        list_frame = tk.Frame(self.classes_window, bg=self.styles.COLORS['background'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=10)
        
        for i, class_obj in enumerate(classes):
            class_frame = tk.Frame(list_frame, 
                                  bg=self.styles.COLORS['light'], 
                                  relief=tk.RIDGE, 
                                  borderwidth=1)
            class_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(class_frame,
                    text=f"📚 {class_obj.name}",
                    font=self.styles.FONTS['normal'],
                    bg=self.styles.COLORS['light']).pack(side=tk.LEFT, padx=10, pady=10)
            
            # Кнопка перегляду учнів
            def view_students(class_id=class_obj.id, class_name=class_obj.name):
                self.app.show_class_students(class_id, class_name)
            
            tk.Button(class_frame,
                     text="Переглянути учнів",
                     font=self.styles.FONTS['small'],
                     bg=self.styles.COLORS['primary'],
                     fg='white',
                     command=view_students).pack(side=tk.RIGHT, padx=10, pady=10)