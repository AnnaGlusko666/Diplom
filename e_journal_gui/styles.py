"""
Стилі та кольори для графічного інтерфейсу
"""

class AppStyles:
    """Клас для зберігання стилів додатку"""
    
    # Кольорова схема
    COLORS = {
        'primary': '#4a6fa5',      # Синій
        'secondary': '#6c757d',    # Сірий
        'success': '#28a745',      # Зелений
        'danger': '#dc3545',       # Червоний
        'warning': '#ffc107',      # Жовтий
        'info': '#17a2b8',         # Бірюзовий
        'light': '#f8f9fa',        # Світлий
        'dark': '#343a40',         # Темний
        'background': '#f0f0f0'    # Фон
    }
    
    # Шрифти
    FONTS = {
        'title': ('Arial', 24, 'bold'),
        'header': ('Arial', 16, 'bold'),
        'normal': ('Arial', 12),
        'small': ('Arial', 10)
    }
    
    @classmethod
    def get_color(cls, color_name):
        """Отримати колір за назвою"""
        return cls.COLORS.get(color_name, cls.COLORS['primary'])
    
    @classmethod
    def get_font(cls, font_name):
        """Отримати шрифт за назвою"""
        return cls.FONTS.get(font_name, cls.FONTS['normal'])
    
    @classmethod
    def configure_button(cls, button, style='primary'):
        """Налаштувати кнопку"""
        color = cls.get_color(style)
        button.config(
            bg=color,
            fg='white',
            font=('Arial', 11, 'bold'),
            relief='raised',
            borderwidth=2,
            padx=10,
            pady=5
        )
    
    @classmethod
    def configure_label(cls, label, style='normal'):
        """Налаштувати мітку"""
        font = cls.get_font(style)
        label.config(
            font=font,
            bg=cls.COLORS['background']
        )