from enum import Enum, unique

# This type represent in what stage company is now
# None means, company is not initialized properly or it has no stocks
# Open means, that everyone can buy stocks
# Closed means, that company is kind on investing process, and only few users can buy it
class CompanyType(Enum):
    NONE = 0
    OPEN = 1
    CLOSED = 2

@unique
class CompanyBusinessType(Enum):
    MILITARY = 1
    ENTERTAINMENT = 2
    SCIENCE = 3
    SOCIAL = 4

# To report result about stock purchase
@unique
class StockPurchaseResult(Enum):
    SUCCESS = 1
    NO_SUCH_COMPANY = 2
    NO_MORE_STOCKS = 3
    NOT_ENOUGH_MONEY = 4
    STOCK_COST_ERROR = 5
    STOCK_AMOUNT_ERROR = 6 # When player requested wrong stock amount

@unique
class StockSellResult(Enum):
    SUCCESS = 1
    NO_SUCH_COMPANY = 2 # No such uuid of company on server
    HAS_NO_COMPANY = 3 # No such uuid of compnay in player data
    NO_ENOUGH_AMOUNT = 4
