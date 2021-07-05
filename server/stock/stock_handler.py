from stock.stock import Stock, StockType

class StockHandler():
    # Singleton part
    __instance = None
    @staticmethod

    def Instance():
        if StockHandler.__instance == None:
            StockHandler()
        return StockHandler.__instance

    def __init__(self):
        StockHandler.__instance = self

    def create_stock(self, c_uuid: str, stock_type : StockType, value: float, owner_id = "") -> Stock:
        stock = Stock(c_uuid,stock_type,value)
        # If owner id is not specified, means that created stock, and server owns it. Stock by default attached to server
        if owner_id != "" :
            stock.buy_stock(owner_id)
        # TODO: Place to store stock in db

        # Return stock
        return stock

    # Mediator method to handle buy stock. To work with database
    def buy_stock(self, stock: Stock, new_owner_uuid: str):
        stock.buy_stock(new_owner_uuid)

    # Remove owner from stock. Basically method for silver stocks
    def sell_stock(self, stock: Stock):
        stock.sell_stock()
