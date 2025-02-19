import re
from datetime import datetime
from django.core.exceptions import ValidationError

def is_valid_phone_number(phone_number):
    # الگوی شماره موبایل افغانستان
    pattern = r"^07[0-9]{8}$"
    
    # بررسی تطابق با الگو
    if re.match(pattern, phone_number):
        return phone_number
    else:
        raise ValueError("The phone number must be correct.")

def is_valid_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$"
    return bool(re.match(pattern, password))

def is_valid_birth_date(value):
    # الگوی تاریخ تولد به‌فرمت YYYY-MM-DD
    pattern = r'^(19[2-9][0-9]|200[0-7])-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'
    
    # بررسی الگوی تاریخ تولد
    if not re.match(pattern, value):
        raise ValidationError("Invalid date format. Use YYYY-MM-DD.")
    
    # محاسبه سن کاربر
    birth_date = datetime.strptime(value, '%Y-%m-%d')
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    # بررسی سن بین 18 تا 100 سال
    if age < 18 or age > 100:
        raise ValidationError("Your age must be between 18 and 100 years.")