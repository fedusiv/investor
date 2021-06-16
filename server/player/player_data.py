from stock.stock import Stock, StockType
import config

# Store stocks by it affiliance to company
class StockStorageElement():
    def __init__(self, company_uuid : str, company_name = "This is Error message"):
        self.company_uuid = company_uuid
        self.company_name = company_name
        self.stock_list_silver = []
        self.stock_list_gold = []

# Handle player data.
class PlayerData():

    @property
    def money(self):
        return self.__money

    def __init__(self):
        self.__money = config.PLAYER_DEFAULT_MONEY_AMOUNT
        self.__stocks  = []

    # Prepare data for info about money amount and stocks money value, that player has
    def get_player_value_info(self):
        stocks_sum = 0
        for element in self.__stocks:
            element : StockStorageElement
            sil_sum = sum(x.cost for x in element.stock_list_silver)
            gold_sum = sum(x.cost for x in element.stock_list_gold)
            stocks_sum += sil_sum + gold_sum
        data = {
                "stocks" : stocks_sum,
                "money" : self.money
                }
        return data


    # As a preview of all money and value that player has
    def get_all_stocks_to_list(self) -> list:
        stocks_list = []
        if len(self.__stocks) < 1:
            return stocks_list

        for element in self.__stocks:
            element: StockStorageElement
            player_is_owner = False
            amount_silver = len(element.stock_list_silver)
            amount_gold = len(element.stock_list_gold)
            # silver stocks
            stocks_cost = []
            stocks_value = []
            for stock in element.stock_list_silver:
                stocks_cost.append(stock.cost)
                stocks_value.append(stock.value)
            silver_cost_sum = sum(stocks_cost)
            silver_value_sum = sum(stocks_value)
            # gold stocks
            for stock in element.stock_list_gold:
                stocks_cost.append(stock.cost)
                stocks_value.append(stock.value)
                if stock.is_main:
                    player_is_owner = True
            gold_cost_sum = sum(stocks_cost)
            gold_value_sum = sum(stocks_value)

            silver_body = {
                    "amount" : amount_silver,
                    "cost" : silver_cost_sum,
                    "value" : silver_value_sum
                }
            gold_body = {
                    "amount" : amount_gold,
                    "cost" : gold_cost_sum,
                    "value" : gold_value_sum,
                    "owner" : player_is_owner
                }
            # Info syntax is based on communication protocol txt
            company_info = {
                'uuid' : element.company_uuid,
                'name' : element.company_name,
                'silver': silver_body,
                'gold' : gold_body
            }
            stocks_list.append(company_info)

        return stocks_list

    # Get amount of silver stocks of certain company. Returns amount of stocks
    # If there is no such company in player data returns -1
    def get_silver_amount_of_company(self,company_uuid: str) -> int:
        res = -1
        for element in self.__stocks:
            element: StockStorageElement
            if element.company_uuid == company_uuid:
                res = len(element.stock_list_silver)
                break
        return res

    # Be aware, this method should be called only after you have confirmation from comnapies handler or logic handler
    def purchase_stock_confirm(self, company_uuid : str, company_name: str, stock_list : list, cost: float):
        # decrease amount of money
        self.__money -= cost

        element = self.get_storage_element_by_uuid(company_uuid)
        if element is None:
                element = StockStorageElement(company_uuid,company_name)
                self.__stocks.append(element)

        for stock in stock_list:
            stock : Stock
            if stock.type == StockType.SILVER:
                element.stock_list_silver.append(stock)
            else:
                element.stock_list_gold.append(stock)


    def get_storage_element_by_uuid(self, company_uuid: str):
        el = None
        for element in self.__stocks:
            element : StockStorageElement
            if element.company_uuid == company_uuid:
                el = element
                break
        return el

    # Sell stocks of given company
    # Be aware this method awaits, that client has required amount of stocks. And even has this company in data
    def sell_silver_stocks(self, company_uuid: str, amount : int, cost : float):
        elem = None
        index = -1
        for element in self.__stocks:
            element: StockStorageElement
            if element.company_uuid == company_uuid:
                elem = element
                index = self.__stocks.index(elem)
                break
        for stock in list(elem.stock_list_silver):
            stock : Stock
            if stock.type == StockType.SILVER:
                stock.sell_stock()# change stock type. Player stores only references to stocks.
                elem.stock_list_silver.remove(stock)
                amount-=1
                if amount <= 0:
                    # Required amount of stock were removed from data
                    break
        if len(elem.stock_list_silver) <= 0:
            # If there is no stock of this company left on player need to remove it from player data
            if index != -1:
                del self.__stocks[index]

        # Increase money amount
        self.__money += cost

