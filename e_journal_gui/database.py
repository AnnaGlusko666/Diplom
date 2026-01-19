"""
Модуль для роботи з JSON базою даних
"""

import json
import os
import hashlib
from typing import List, Dict, Optional
from datetime import datetime
from models import *

class Database:
    def __init__(self):
        self.data_dir = "data"
        self.files = {
            'users': 'users.json',
            'classes': 'classes.json',
            'grades': 'grades.json',
            'profiles': 'student_profiles.json',
            'shop': 'shop_items.json',
            'badges': 'badges.json'
        }
        self.initialize()
    
    def initialize(self) -> bool:
        """Ініціалізація бази даних"""
        try:
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
            
            for filename in self.files.values():
                filepath = os.path.join(self.data_dir, filename)
                if not os.path.exists(filepath):
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump([], f, ensure_ascii=False, indent=2)
            
            self._create_default_data()
            return True
        
        except Exception as e:
            print(f"Помилка ініціалізації бази даних: {e}")
            return False
    
    def _create_default_data(self):
        """Створення тестових даних"""
        # Тестовий адміністратор
        if not self.get_user_by_username('admin'):
            admin = User(
                id=generate_id(),
                username='admin',
                password_hash=self._hash_password('admin123'),
                full_name='Адміністратор Системи',
                user_type=UserType.TEACHER
            )
            self.save_user(admin)
        
        # Відзнаки
        badges = self._load_data('badges.json')
        if not badges:
            default_badges = [
                Badge(
                    id=generate_id(),
                    name='Перша відмінна оцінка',
                    description='Отримайте оцінку 12',
                    rarity=BadgeRarity.COMMON,
                    icon='⭐',
                    condition={'type': 'first_12'},
                    coins_reward=10
                ),
                Badge(
                    id=generate_id(),
                    name='Відмінник тижня',
                    description='5 оцінок 10+ за тиждень',
                    rarity=BadgeRarity.RARE,
                    icon='👑',
                    condition={'type': 'weekly_excellent'},
                    coins_reward=25
                ),
                Badge(
                    id=generate_id(),
                    name='Майстер математики',
                    description='Середній бал 10+ з математики',
                    rarity=BadgeRarity.EPIC,
                    icon='🎯',
                    condition={'type': 'subject_master'},
                    coins_reward=50
                )
            ]
            self._save_data('badges.json', [b.to_dict() for b in default_badges])
        
        # Товари магазину
        shop_items = self._load_data('shop.json')
        if not shop_items:
            default_items = [
                ShopItem(
                    id=generate_id(),
                    name='Кольоровий аватар',
                    description='Спеціальний аватар',
                    price=50,
                    category='avatar',
                    data={'avatar_type': 'colorful'}
                ),
                ShopItem(
                    id=generate_id(),
                    name='Додатковий бал',
                    description='+1 бал до будь-якої оцінки',
                    price=100,
                    category='privilege',
                    data={'privilege_type': 'extra_point'}
                ),
                ShopItem(
                    id=generate_id(),
                    name='Золота рамка',
                    description='Ексклюзивна рамка профілю',
                    price=200,
                    category='profile_item',
                    data={'item_type': 'gold_frame'}
                )
            ]
            self._save_data('shop.json', [i.to_dict() for i in default_items])
    
    def _hash_password(self, password: str) -> str:
        """Хешування пароля"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _load_data(self, filename: str) -> List[Dict]:
        """Завантаження даних з JSON файлу"""
        try:
            filepath = os.path.join(self.data_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_data(self, filename: str, data: List[Dict]) -> bool:
        """Збереження даних у JSON файл"""
        try:
            filepath = os.path.join(self.data_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Помилка збереження даних: {e}")
            return False
    
    # === МЕТОДИ ДЛЯ КОРИСТУВАЧІВ ===
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        users_data = self._load_data('users.json')
        for user_data in users_data:
            if user_data['username'] == username:
                return User.from_dict(user_data)
        return None
    
    def save_user(self, user: User) -> bool:
        users_data = self._load_data('users.json')
        
        for i, u in enumerate(users_data):
            if u['id'] == user.id:
                users_data[i] = user.to_dict()
                break
        else:
            users_data.append(user.to_dict())
        
        return self._save_data('users.json', users_data)
    
    def get_student_by_id(self, student_id: str) -> Optional[User]:
        users_data = self._load_data('users.json')
        for user_data in users_data:
            if user_data['id'] == student_id and user_data['user_type'] == 'student':
                return User.from_dict(user_data)
        return None
    
    def get_teacher_by_id(self, teacher_id: str) -> Optional[User]:
        users_data = self._load_data('users.json')
        for user_data in users_data:
            if user_data['id'] == teacher_id and user_data['user_type'] == 'teacher':
                return User.from_dict(user_data)
        return None
    
    # === МЕТОДИ ДЛЯ КЛАСІВ ===
    
    def create_class(self, name: str, teacher_id: str) -> Optional[Class]:
        new_class = Class(
            id=generate_id(),
            name=name,
            class_teacher_id=teacher_id
        )
        
        classes_data = self._load_data('classes.json')
        classes_data.append(new_class.to_dict())
        
        if self._save_data('classes.json', classes_data):
            return new_class
        return None
    
    def get_teacher_classes(self, teacher_id: str) -> List[Class]:
        classes_data = self._load_data('classes.json')
        teacher_classes = []
        
        for class_data in classes_data:
            if class_data['class_teacher_id'] == teacher_id:
                teacher_classes.append(Class.from_dict(class_data))
        
        return teacher_classes
    
    def get_class_by_id(self, class_id: str) -> Optional[Class]:
        classes_data = self._load_data('classes.json')
        for class_data in classes_data:
            if class_data['id'] == class_id:
                return Class.from_dict(class_data)
        return None
    
    def add_student_to_class(self, class_id: str, student_id: str) -> bool:
        classes_data = self._load_data('classes.json')
        
        for class_data in classes_data:
            if class_data['id'] == class_id:
                if student_id not in class_data['student_ids']:
                    class_data['student_ids'].append(student_id)
                    return self._save_data('classes.json', classes_data)
                return True  # Вже доданий
        
        return False
    
    def get_students_in_class(self, class_id: str) -> List[User]:
        class_data = self.get_class_by_id(class_id)
        if not class_data:
            return []
        
        students = []
        for student_id in class_data.student_ids:
            student = self.get_student_by_id(student_id)
            if student:
                students.append(student)
        
        return students
    
    # === МЕТОДИ ДЛЯ ОЦІНОК ===
    
    def get_student_grades(self, student_id: str) -> List[Grade]:
        grades_data = self._load_data('grades.json')
        student_grades = []
        
        for grade_data in grades_data:
            if grade_data['student_id'] == student_id:
                student_grades.append(Grade.from_dict(grade_data))
        
        return student_grades
    
    def add_grade(self, grade: Grade) -> bool:
        grades_data = self._load_data('grades.json')
        grades_data.append(grade.to_dict())
        return self._save_data('grades.json', grades_data)
    
    # === МЕТОДИ ДЛЯ ПРОФІЛІВ УЧНІВ ===
    
    def get_student_profile(self, student_id: str) -> StudentProfile:
        profiles_data = self._load_data('profiles.json')
        
        for profile_data in profiles_data:
            if profile_data['student_id'] == student_id:
                return StudentProfile.from_dict(profile_data)
        
        # Створення нового профілю
        new_profile = StudentProfile(student_id=student_id)
        profiles_data.append(new_profile.to_dict())
        self._save_data('profiles.json', profiles_data)
        return new_profile
    
    def save_student_profile(self, profile: StudentProfile) -> bool:
        profiles_data = self._load_data('profiles.json')
        
        for i, p in enumerate(profiles_data):
            if p['student_id'] == profile.student_id:
                profiles_data[i] = profile.to_dict()
                break
        else:
            profiles_data.append(profile.to_dict())
        
        return self._save_data('profiles.json', profiles_data)
    
    # === МЕТОДИ ДЛЯ МАГАЗИНУ ===
    
    def get_shop_items(self) -> List[ShopItem]:
        items_data = self._load_data('shop.json')
        return [ShopItem.from_dict(item) for item in items_data if not item.get('teacher_only', False)]
    
    def purchase_item(self, student_id: str, item_id: str, price: int) -> bool:
        profile = self.get_student_profile(student_id)
        
        if profile.coins < price:
            return False
        
        profile.coins -= price
        profile.bought_items.append(item_id)
        return self.save_student_profile(profile)
    
    # === МЕТОДИ ДЛЯ ВІДЗНАК ===
    
    def get_all_badges(self) -> List[Badge]:
        badges_data = self._load_data('badges.json')
        return [Badge.from_dict(badge) for badge in badges_data]
    # Додати ці методи в клас Database:

def add_subject_teacher(self, class_id: str, teacher_id: str, subject: str) -> bool:
    """Додати вчителя-предметника до класу"""
    classes_data = self._load_data('classes.json')
    
    for class_data in classes_data:
        if class_data['id'] == class_id:
            if subject not in class_data['subject_teachers']:
                class_data['subject_teachers'][subject] = []
            
            if teacher_id not in class_data['subject_teachers'][subject]:
                class_data['subject_teachers'][subject].append(teacher_id)
            
            return self._save_data('classes.json', classes_data)
    
    return False

def get_subject_teachers(self, class_id: str) -> Dict[str, List[str]]:
    """Отримати вчителів-предметників класу"""
    class_data = self.get_class_by_id(class_id)
    if class_data:
        return class_data.subject_teachers
    return {}

def is_class_teacher(self, class_id: str, teacher_id: str) -> bool:
    """Перевірити чи вчитель є класним керівником"""
    class_data = self.get_class_by_id(class_id)
    if class_data:
        return class_data.class_teacher_id == teacher_id
    return False

def get_student_purchases(self, student_id: str) -> List[Dict]:
    """Отримати покупки учня"""
    profile = self.get_student_profile(student_id)
    shop_items = self._load_data('shop.json')
    
    purchases = []
    for item_id in profile.bought_items:
        for item_data in shop_items:
            if item_data['id'] == item_id:
                purchases.append(item_data)
                break
    
    return purchases

def get_teacher_items(self, teacher_id: str) -> List[ShopItem]:
    """Отримати товари вчителя"""
    shop_items = self._load_data('shop.json')
    teacher_items = []
    
    for item_data in shop_items:
        if item_data.get('teacher_id') == teacher_id:
            teacher_items.append(ShopItem.from_dict(item_data))
    
    return teacher_items