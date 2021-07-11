from enum import Enum, unique

@unique
class StockType(Enum):
    SILVER = 1 # Silver level is common level of stock. It has cost: (value - all gold stocks)/ amount_of_silver
    GOLD = 2 # Gold has it's own "custom" value. They usually can not be obtain from opensource

@unique
class StockSellResult(Enum):
    SUCCESS = 1
    NO_SUCH_STOCK = 2
