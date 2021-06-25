from stock.stock import Stock, StockType

class StockBuilder():
    # Singleton part
    __instance = None
    @staticmethod

    def Instance():
        if StockBuilder.__instance == None:
            StockBuilder()
        return StockBuilder.__instance

    def __init__(self):
        StockBuilder.__instance = self

    def create_stock(self, c_uuid: str, stock_type : StockType, value: float) -> Stock:
        return Stock(c_uuid,stock_type,value)
