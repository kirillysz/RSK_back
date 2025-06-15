from enum import Enum

class UserEnum(str, Enum):
    Student = "Студент"
    Teacher = "Преподаватель"
    