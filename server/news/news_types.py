# Files stores types classes
from enum import Enum, unique

@unique
class InfluenceStage(Enum):
    NONE = 0
    LOW = 1
    DEFAULT = 2
    CRITICAL = 3

@unique
class NewsTypes(Enum):
    NONE = 0
    WAR = 1
    SCIENCE = 2
    ENTERTAINMENT = 3
    HARDWARE = 4
    SOCIAL = 5
