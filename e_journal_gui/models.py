"""
Моделі даних для електронного журналу
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum
import uuid

class UserType(Enum):
    STUDENT = "student"
    TEACHER = "teacher"

class BadgeRarity(Enum):
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

@dataclass
class User:
    id: str
    username: str
    password_hash: str
    full_name: str
    user_type: UserType
    class_id: Optional[str] = None
    avatar: str = "default"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_login: Optional[str] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password_hash': self.password_hash,
            'full_name': self.full_name,
            'user_type': self.user_type.value,
            'class_id': self.class_id,
            'avatar': self.avatar,
            'created_at': self.created_at,
            'last_login': self.last_login
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            username=data['username'],
            password_hash=data['password_hash'],
            full_name=data['full_name'],
            user_type=UserType(data['user_type']),
            class_id=data.get('class_id'),
            avatar=data.get('avatar', 'default'),
            created_at=data.get('created_at', datetime.now().isoformat()),
            last_login=data.get('last_login')
        )

@dataclass
class StudentProfile:
    student_id: str
    coins: int = 0
    badges: List[str] = field(default_factory=list)
    bought_items: List[str] = field(default_factory=list)
    avatar_items: List[str] = field(default_factory=list)
    total_grades: int = 0
    average_grade: float = 0.0
    
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'coins': self.coins,
            'badges': self.badges,
            'bought_items': self.bought_items,
            'avatar_items': self.avatar_items,
            'total_grades': self.total_grades,
            'average_grade': self.average_grade
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            student_id=data['student_id'],
            coins=data.get('coins', 0),
            badges=data.get('badges', []),
            bought_items=data.get('bought_items', []),
            avatar_items=data.get('avatar_items', []),
            total_grades=data.get('total_grades', 0),
            average_grade=data.get('average_grade', 0.0)
        )

@dataclass
class Grade:
    id: str
    student_id: str
    teacher_id: str
    subject: str
    value: int
    date: str
    comment: Optional[str] = None
    coins_awarded: bool = False
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'teacher_id': self.teacher_id,
            'subject': self.subject,
            'value': self.value,
            'date': self.date,
            'comment': self.comment,
            'coins_awarded': self.coins_awarded
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            student_id=data['student_id'],
            teacher_id=data['teacher_id'],
            subject=data['subject'],
            value=data['value'],
            date=data['date'],
            comment=data.get('comment'),
            coins_awarded=data.get('coins_awarded', False)
        )

@dataclass
class Class:
    id: str
    name: str
    class_teacher_id: str
    subject_teachers: Dict[str, List[str]] = field(default_factory=dict)
    student_ids: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'class_teacher_id': self.class_teacher_id,
            'subject_teachers': self.subject_teachers,
            'student_ids': self.student_ids,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            name=data['name'],
            class_teacher_id=data['class_teacher_id'],
            subject_teachers=data.get('subject_teachers', {}),
            student_ids=data.get('student_ids', []),
            created_at=data.get('created_at', datetime.now().isoformat())
        )

@dataclass
class Badge:
    id: str
    name: str
    description: str
    rarity: BadgeRarity
    icon: str
    condition: Dict
    coins_reward: int
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'rarity': self.rarity.value,
            'icon': self.icon,
            'condition': self.condition,
            'coins_reward': self.coins_reward
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            rarity=BadgeRarity(data['rarity']),
            icon=data['icon'],
            condition=data['condition'],
            coins_reward=data['coins_reward']
        )

@dataclass
class ShopItem:
    id: str
    name: str
    description: str
    price: int
    category: str
    data: Dict
    teacher_only: bool = False
    teacher_id: Optional[str] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'data': self.data,
            'teacher_only': self.teacher_only,
            'teacher_id': self.teacher_id
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            price=data['price'],
            category=data['category'],
            data=data['data'],
            teacher_only=data.get('teacher_only', False),
            teacher_id=data.get('teacher_id')
        )

def generate_id():
    """Генерація унікального ID"""
    return str(uuid.uuid4())