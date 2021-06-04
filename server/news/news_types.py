# Files stores types classes
from enum import Enum, unique

@unique
class NewsTypes(Enum):
    NONE = 0
    WAR = 1
    SCIENCE = 2
    ENTERTAINMENT = 3
    HARDWARE = 4
    SOCIAL = 5
    FINANCIAL = 6
    GRAPHICS = 7
