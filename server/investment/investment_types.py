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

@unique
class InvestmentMakeResult(Enum):
    SUCCESS = 1
    NO_SUCH_INVESTMENT_PLAN = 2
    NO_SUCH_COMPANY = 3
    NOT_ENOUGH_MONEY = 4
    NO_PLAN_IN_COMPANY = 5
