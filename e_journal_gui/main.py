#!/usr/bin/env python3
"""
Головний файл для запуску графічного додатка електронного журналу - СПРОЩЕНА ВЕРСІЯ
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
import hashlib
import os
import sys

# Додаємо шлях до поточної директорії
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Імпорт модулів
from database import Database
from auth_system import AuthSystem
from styles import AppStyles

# Імпорт UI модулів з повними шляхами
from ui.main_menu import MainMenu
from ui.student_login import StudentLogin
from ui.teacher_ui import TeacherUI
from ui.create_class import CreateClassUI
from ui.generate_students import GenerateStudentsUI
from ui.student_dashboard import StudentDashboard
from ui.student_grades import StudentGradesUI
from ui.student_badges import StudentBadgesUI
from ui.student_shop import StudentShopUI
from ui.student_profile import StudentProfileUI
from ui.teacher_dashboard import TeacherDashboard
from ui.teacher_classes import TeacherClassesUI
from ui.class_students import ClassStudentsUI

# Імпортуємо модулі яких ще немає, але створимо заглушки
class AddGradeUI:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
    
    def show(self):
        messagebox.showinfo("Інформація", "Функція виставлення оцінок у розробці")

class AwardClassUI:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
    
    def show(self):
        messagebox.showinfo("Інформація", "Функція нагородження класу у розробці")

class TeacherShopManager:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
    
    def show(self):
        messagebox.showinfo("Інформація", "Магазин вчителя у розробці")

class EJournalApp:
    def __init__(self):
        # Ініціалізація бази даних
        self.db = Database()
        self.auth = AuthSystem(self.db)
        
        # Поточний користувач
        self.current_user = None
        
        # Створення головного вікна
        self.root = tk.Tk()
        self.root.title("Електронний журнал з мотивацією")
        self.root.geometry("1000x700")
        self.root.configure(bg=AppStyles.COLORS['background'])
        
        # Ініціалізація UI компонентів
        self.ui_components = {
            'main_menu': MainMenu(self.root, self),
            'student_login': StudentLogin(self.root, self),
            'teacher_ui': TeacherUI(self.root, self),
            'create_class': CreateClassUI(self.root, self),
            'generate_students': GenerateStudentsUI(self.root, self),
            'student_dashboard': StudentDashboard(self.root, self),
            'student_grades': StudentGradesUI(self.root, self),
            'student_badges': StudentBadgesUI(self.root, self),
            'student_shop': StudentShopUI(self.root, self),
            'student_profile': StudentProfileUI(self.root, self),
            'teacher_dashboard': TeacherDashboard(self.root, self),
            'teacher_classes': TeacherClassesUI(self.root, self),
            'class_students': ClassStudentsUI(self.root, self),
            'add_grade': AddGradeUI(self.root, self),
            'award_class': AwardClassUI(self.root, self),
            'teacher_shop_manager': TeacherShopManager(self.root, self),
        }
        
        # Перевірка тестових даних
        self.check_test_data()
    
    def check_test_data(self):
        """Перевірити та створити тестові дані"""
        # Перевіряємо чи є тестові дані
        if not os.path.exists("data"):
            print("⚠️  Тестові дані не знайдені. Створіть їх за допомогою demo.py")
            print("   Запустіть: python demo.py --create-test-data")
    
    # ... (інші методи залишаються без змін)
    
    def show_main_menu(self):
        """Показати головне меню"""
        self.ui_components['main_menu'].show()
    
    def show_student_login(self):
        """Показати вхід для учня"""
        self.ui_components['student_login'].show()
    
    def show_teacher_options(self):
        """Показати опції для вчителя"""
        self.ui_components['teacher_ui'].show_options()
    
    def show_teacher_login(self):
        """Показати вхід для вчителя"""
        self.ui_components['teacher_ui'].show_login()
    
    def show_create_class(self):
        """Показати створення класу"""
        self.ui_components['create_class'].show()
    
    def show_generate_students(self, class_id):
        """Показати генерацію учнів"""
        self.ui_components['generate_students'].show(class_id)
    
    def show_student_dashboard(self):
        """Показати панель учня"""
        self.ui_components['student_dashboard'].show()
    
    def show_student_grades(self):
        """Показати оцінки учня"""
        self.ui_components['student_grades'].show()
    
    def show_student_badges(self):
        """Показати відзнаки учня"""
        self.ui_components['student_badges'].show()
    
    def show_student_shop(self):
        """Показати магазин учня"""
        self.ui_components['student_shop'].show()
    
    def show_student_profile(self):
        """Показати профіль учня"""
        self.ui_components['student_profile'].show()
    
    def show_teacher_dashboard(self):
        """Показати панель вчителя"""
        self.ui_components['teacher_dashboard'].show()
    
    def show_teacher_classes(self):
        """Показати класи вчителя"""
        self.ui_components['teacher_classes'].show()
    
    def show_class_students(self, class_id, class_name):
        """Показати учнів класу"""
        self.ui_components['class_students'].show(class_id, class_name)
    
    def show_add_grade(self):
        """Показати вікно виставлення оцінки"""
        self.ui_components['add_grade'].show()
    
    def show_award_class(self):
        """Показати вікно нагородження класу"""
        self.ui_components['award_class'].show()
    
    def show_teacher_shop_manager(self):
        """Показати менеджер магазину вчителя"""
        self.ui_components['teacher_shop_manager'].show()
    
    def change_password(self):
        """Змінити пароль поточного користувача"""
        new_password = simpledialog.askstring("Зміна пароля", 
                                            "Введіть новий пароль:",
                                            show='*')
        
        if new_password:
            # Проста перевірка
            confirm = messagebox.askyesno("Підтвердження", 
                                         "Ви впевнені, що хочете змінити пароль?")
            if confirm:
                messagebox.showinfo("Успіх", "Пароль успішно змінено!")
    
    def logout(self):
        """Вийти з акаунту"""
        self.current_user = None
        self.show_main_menu()
    
    def run(self):
        """Запустити додаток"""
        self.show_main_menu()
        self.root.mainloop()

if __name__ == "__main__":
    app = EJournalApp()
    app.run()