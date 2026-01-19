"""
Модуль автентифікації та реєстрації користувачів - ОНОВЛЕНИЙ
"""

import hashlib
import random
import string
from typing import List, Optional
from datetime import datetime
from models import User, UserType, generate_id
from database import Database
from tkinter import messagebox

class AuthSystem:
    def __init__(self, db: Database):
        self.db = db
    
    def hash_password(self, password: str) -> str:
        """Хешування пароля"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def generate_student_username(self, full_name: str, class_name: str) -> str:
        """Генерація логіна для учня"""
        name_parts = full_name.split()
        if len(name_parts) >= 2:
            first_letter = name_parts[0][0].lower()
            last_name = name_parts[-1].lower().replace(' ', '')
            
            # Вилучення цифр з назви класу
            class_number = ''.join(filter(str.isdigit, class_name))
            if not class_number:
                class_number = "10"
            
            # Заміна українських літер
            ukrainian_to_latin = {
                'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g',
                'д': 'd', 'е': 'e', 'є': 'ye', 'ж': 'zh', 'з': 'z',
                'и': 'y', 'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k',
                'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
                'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
                'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
                'ь': '', 'ю': 'yu', 'я': 'ya'
            }
            
            # Конвертація прізвища
            converted_last_name = ''
            for char in last_name:
                if char in ukrainian_to_latin:
                    converted_last_name += ukrainian_to_latin[char]
                else:
                    converted_last_name += char
            
            base_username = f"{first_letter}{converted_last_name}{class_number}"
        else:
            base_username = full_name.lower().replace(' ', '') + "10"
        
        # Перевірка унікальності
        username = base_username
        counter = 1
        while self.db.get_user_by_username(username):
            username = f"{base_username}{counter}"
            counter += 1
        
        return username
    
    def generate_student_password(self, length: int = 8) -> str:
        """Генерація випадкового пароля для учня"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def login(self, username: str, password: str, user_type: str) -> Optional[User]:
        """Вхід в систему"""
        password_hash = self.hash_password(password)
        user = self.db.get_user_by_username(username)
        
        if not user:
            return None
        
        # Перевірка типу користувача
        if user_type == "student" and user.user_type != UserType.STUDENT:
            return None
        elif user_type == "teacher" and user.user_type != UserType.TEACHER:
            return None
        
        # Перевірка пароля
        if user.password_hash == password_hash:
            # Оновлення часу останнього входу
            user.last_login = datetime.now().isoformat()
            self.db.save_user(user)
            return user
        
        return None
    
    def register_teacher(self, full_name: str, username: str, password: str) -> Optional[User]:
        """Реєстрація нового вчителя"""
        # Перевірка чи існує користувач
        existing = self.db.get_user_by_username(username)
        if existing:
            messagebox.showerror("Помилка", "Користувач з таким логіном вже існує!")
            return None
        
        # Створення вчителя
        teacher = User(
            id=generate_id(),
            username=username,
            password_hash=self.hash_password(password),
            full_name=full_name,
            user_type=UserType.TEACHER
        )
        
        if self.db.save_user(teacher):
            return teacher
        
        return None
    
    def generate_student_accounts(self, class_id: str, student_names: List[str]) -> List[dict]:
        """Генерація акаунтів для учнів класу"""
        credentials = []
        class_info = self.db.get_class_by_id(class_id)
        
        if not class_info:
            messagebox.showerror("Помилка", "Клас не знайдений!")
            return []
        
        for name in student_names:
            # Генерація унікального логіна та пароля
            username = self.generate_student_username(name, class_info.name)
            password = self.generate_student_password()
            
            # Створення учня
            student = User(
                id=generate_id(),
                username=username,
                password_hash=self.hash_password(password),
                full_name=name,
                user_type=UserType.STUDENT,
                class_id=class_id
            )
            
            if self.db.save_user(student):
                # Автоматично створює профіль
                self.db.get_student_profile(student.id)
                
                # Додавання учня до класу
                self.db.add_student_to_class(class_id, student.id)
                
                credentials.append({
                    'id': student.id,
                    'full_name': name,
                    'username': username,
                    'password': password,
                    'class_id': class_id
                })
        
        return credentials