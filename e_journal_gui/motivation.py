"""
Модуль мотиваційної системи
"""

from typing import List, Dict
from datetime import datetime, timedelta
from models import Grade, StudentProfile, Badge, UserType
from database import Database
from tkinter import messagebox

class MotivationSystem:
    def __init__(self, db: Database):
        self.db = db
    
    def calculate_coins_for_grade(self, grade_value: int) -> int:
        """Розрахунок монет за оцінку"""
        if grade_value == 12:
            return 5
        elif grade_value >= 10:
            return 3
        elif grade_value >= 8:
            return 2
        elif grade_value >= 6:
            return 1
        elif grade_value <= 3:
            return -2  # Штраф за низьку оцінку
        else:
            return 0
    
    def add_grade_with_motivation(self, grade: Grade) -> bool:
        """Додати оцінку з автоматичним нарахуванням монет"""
        # Додаємо оцінку
        if not self.db.add_grade(grade):
            return False
        
        # Нараховуємо монети
        coins = self.calculate_coins_for_grade(grade.value)
        if coins != 0:
            profile = self.db.get_student_profile(grade.student_id)
            profile.coins += coins
            self.db.save_student_profile(profile)
            
            # Позначаємо що монети нараховані
            grade.coins_awarded = True
        
        # Перевіряємо відзнаки
        self.check_badges_for_student(grade.student_id)
        
        return True
    
    def check_badges_for_student(self, student_id: str):
        """Перевірити та видати відзнаки учню"""
        student_grades = self.db.get_student_grades(student_id)
        profile = self.db.get_student_profile(student_id)
        all_badges = self.db.get_all_badges()
        
        earned_badges = []
        
        for badge in all_badges:
            if badge.id in profile.badges:
                continue  # Відзнака вже отримана
            
            if self.check_badge_conditions(badge, student_grades, profile):
                # Видаємо відзнаку
                profile.badges.append(badge.id)
                profile.coins += badge.coins_reward
                earned_badges.append(badge)
        
        if earned_badges:
            self.db.save_student_profile(profile)
            # Можна додати сповіщення про отримання відзнак
    
    def check_badge_conditions(self, badge: Badge, grades: List[Grade], profile: StudentProfile) -> bool:
        """Перевірити умови отримання відзнаки"""
        condition_type = badge.condition.get('type')
        
        if condition_type == 'first_12':
            # Перша оцінка 12
            for grade in grades:
                if grade.value == 12:
                    return True
            return False
        
        elif condition_type == 'weekly_excellent':
            # 5 оцінок 10+ за поточний тиждень
            count_needed = badge.condition.get('count', 5)
            week_ago = datetime.now() - timedelta(days=7)
            
            excellent_grades = [
                g for g in grades 
                if datetime.fromisoformat(g.date.replace('Z', '+00:00')) >= week_ago 
                and g.value >= 10
            ]
            
            return len(excellent_grades) >= count_needed
        
        elif condition_type == 'subject_master':
            # Майстер предмета
            subject = badge.condition.get('subject')
            min_avg = badge.condition.get('min_avg', 10)
            
            subject_grades = [g for g in grades if g.subject == subject]
            if not subject_grades:
                return False
            
            avg = sum(g.value for g in subject_grades) / len(subject_grades)
            return avg >= min_avg
        
        elif condition_type == 'coins_collected':
            # Зібрати певну кількість монет
            coins_needed = badge.condition.get('coins', 100)
            return profile.coins >= coins_needed
        
        return False
    
    def award_coins_to_class(self, class_id: str, teacher_id: str, coins: int, reason: str):
        """Нагородити весь клас монетами"""
        students = self.db.get_students_in_class(class_id)
        results = []
        
        for student in students:
            profile = self.db.get_student_profile(student.id)
            profile.coins += coins
            self.db.save_student_profile(profile)
            
            # Додаємо запис про нагороду (можна зберігати в окремій таблиці)
            results.append({
                'student_id': student.id,
                'student_name': student.full_name,
                'coins_awarded': coins,
                'reason': reason,
                'teacher_id': teacher_id,
                'date': datetime.now().isoformat()
            })
        
        return results
    
    def get_leaderboard(self, class_id: str) -> List[Dict]:
        """Отримати рейтинг учнів класу"""
        students = self.db.get_students_in_class(class_id)
        leaderboard = []
        
        for student in students:
            profile = self.db.get_student_profile(student.id)
            leaderboard.append({
                'student_id': student.id,
                'full_name': student.full_name,
                'coins': profile.coins,
                'badges_count': len(profile.badges),
                'average_grade': profile.average_grade,
                'avatar': student.avatar
            })
        
        # Сортування за монетами
        leaderboard.sort(key=lambda x: x['coins'], reverse=True)
        
        # Додаємо місця
        for i, entry in enumerate(leaderboard):
            entry['rank'] = i + 1
        
        return leaderboard