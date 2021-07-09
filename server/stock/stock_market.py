from typing import TypedDict
from stock.stock import Stock


class StockMarketElement(TypedDict):
    time : float # Time when stock was added to Market
    cost : float # cost of stock
    player_uuid : str
    stock : Stock

class StockMarket():
    # Singleton part
    __instance = None
    @staticmethod

    def Instance():
        if StockMarket.__instance == None:
            StockMarket()
        return StockMarket.__instance

    def __init__(self):
        StockMarket.__instance = self
        self._market_storage = []


    # Formulate message for server to send market information
    # Align this part with communication protocol
    def get_market_list(self):
        market_list = []
        for element in self._market_storage:
            element : StockMarketElement
            data = {
                    "time" : element["time"],
                    "cost" : element["cost"],
                    "p_uuid" : element["player_uuid"],
                    "c_uuid" : element["stock"].company_uuid,
                    "value" : element["stock"].value
                    }
            market_list.append(data)
        body = {
                "amount" : len(market_list),
                "list" : market_list
                }
        return body

    def sell_on_market(self, server_time: float, cost: float, player_uuid: str, stock: Stock):
        element = StockMarketElement(time=server_time, cost=cost,player_uuid=player_uuid,stock=stock)
        self._market_storage.append(element)


