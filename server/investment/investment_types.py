# File with Enums and different types for investment module
from enum import Enum, unique

@unique
class InvestmentType(Enum):
    NONE = 0
    CONST = 1
    PERCENTAGE = 2

@unique
class InvestmentPlanCreateResult(Enum):
    SUCCESS = 1
    NO_SUCH_COMPANY = 2
    NOT_OWNER = 3
