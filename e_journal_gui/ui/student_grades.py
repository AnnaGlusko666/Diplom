"""
Вікно перегляду оцінок учня
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from styles import AppStyles

class StudentGradesUI:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.styles = AppStyles
        
    def show(self):
        """Показати оцінки учня"""
        grades = self.app.db.get_student_grades(self.app.current_user.id)
        
        # Створення нового вікна
        self.grades_window = tk.Toplevel(self.root)
        self.grades_window.title("Мої оцінки")
        self.grades_window.geometry("800x600")
        self.grades_window.configure(bg=self.styles.COLORS['background'])
        
        # Заголовок
        tk.Label(self.grades_window,
                text="МОЇ ОЦІНКИ",
                font=self.styles.FONTS['title'],
                fg=self.styles.COLORS['primary'],
                bg=self.styles.COLORS['background']).pack(pady=20)
        
        if not grades:
            tk.Label(self.grades_window,
                    text="У вас ще немає оцінок",
                    font=self.styles.FONTS['normal'],
                    fg=self.styles.COLORS['secondary'],
                    bg=self.styles.COLORS['background']).pack(pady=50)
        else:
            # Сітка для оцінок
            self.create_grades_display(grades)
    
    def create_grades_display(self, grades):
        """Створити відображення оцінок"""
        canvas = tk.Canvas(self.grades_window, bg=self.styles.COLORS['background'])
        scrollbar = tk.Scrollbar(self.grades_window, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=self.styles.COLORS['background'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Групування оцінок за предметами
        subjects = {}
        for grade in grades:
            if grade.subject not in subjects:
                subjects[grade.subject] = []
            subjects[grade.subject].append(grade)
        
        row = 0
        for subject, subject_grades in subjects.items():
            # Заголовок предмета
            subject_frame = tk.Frame(self.scrollable_frame, 
                                   bg=self.styles.COLORS['light'], 
                                   relief=tk.RIDGE, 
                                   borderwidth=2)
            subject_frame.grid(row=row, column=0, columnspan=3, sticky='ew', padx=10, pady=5)
            row += 1
            
            tk.Label(subject_frame,
                    text=f"📖 {subject}",
                    font=self.styles.FONTS['header'],
                    bg=self.styles.COLORS['light']).pack(pady=5)
            
            # Оцінки
            for grade in subject_grades:
                grade_frame = tk.Frame(self.scrollable_frame, bg=self.styles.COLORS['background'])
                grade_frame.grid(row=row, column=0, columnspan=3, sticky='ew', padx=20, pady=2)
                row += 1
                
                # Визначення кольору за оцінкою
                if grade.value >= 10:
                    color = self.styles.COLORS['success']
                elif grade.value >= 7:
                    color = self.styles.COLORS['warning']
                else:
                    color = self.styles.COLORS['danger']
                
                tk.Label(grade_frame,
                        text=f"{grade.value}",
                        font=('Arial', 12, 'bold'),
                        fg='white',
                        bg=color,
                        width=4).pack(side=tk.LEFT, padx=5)
                
                # Дата
                try:
                    date_obj = datetime.fromisoformat(grade.date.replace('Z', '+00:00'))
                    date_str = date_obj.strftime("%d.%m.%Y")
                except:
                    date_str = grade.date[:10] if len(grade.date) >= 10 else grade.date
                
                tk.Label(grade_frame,
                        text=f"{date_str}",
                        font=self.styles.FONTS['small'],
                        bg=self.styles.COLORS['background']).pack(side=tk.LEFT, padx=10)
                
                # Коментар
                if grade.comment:
                    tk.Label(grade_frame,
                            text=grade.comment,
                            font=('Arial', 11, 'italic'),
                            fg=self.styles.COLORS['secondary'],
                            bg=self.styles.COLORS['background']).pack(side=tk.LEFT, padx=10)
            
            # Середній бал
            avg = sum(g.value for g in subject_grades) / len(subject_grades)
            avg_frame = tk.Frame(self.scrollable_frame, bg=self.styles.COLORS['background'])
            avg_frame.grid(row=row, column=0, columnspan=3, sticky='ew', padx=20, pady=5)
            row += 1
            
            tk.Label(avg_frame,
                    text=f"Середній бал: {avg:.1f}",
                    font=('Arial', 11, 'bold'),
                    fg=self.styles.COLORS['primary'],
                    bg=self.styles.COLORS['background']).pack()
            
            # Роздільник
            tk.Frame(self.scrollable_frame,
                    height=2,
                    bg=self.styles.COLORS['secondary']).grid(row=row, column=0, columnspan=3, 
                                                           sticky='ew', padx=20, pady=10)
            row += 1
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")