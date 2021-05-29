import time

from tornado import gen

from companies.companies_handler import CompaniesHandler
from news.news_handler import NewsHandler
import config


class LogicHandler():
    # Singleton part
    __instance = None
    @staticmethod

    def Instance():
        if LogicHandler.__instance == None:
            LogicHandler()
        return LogicHandler.__instance

    def __init__(self):
        LogicHandler.__instance = self
        self.companies_handler = CompaniesHandler.Instance()
        self.news_handler = NewsHandler.Instance()

        # Time counters for companies update
        self.last_company_news_update = time.time()
        self.last_company_cost_update = time.time()

    #---------------------#
    #Properties part
    #---------------------#
    @property
    def server_time(self):
        return self.__server_time

    #---------------------#
    #Logic part
    #---------------------#

    # Main loop of logic handler!
    async def logic_loop(self):
        self.__server_start_time = time.time()
        while True:
            # Calculate time
            self.__server_time = time.time() - self.__server_start_time

            self.news_handler.update_news(self.server_time)	# Call news main handler.
            self.companies_handler.update_companies()	# Call companies main handler
            self.companies_changing(self.news_handler.world_situation)	# Call changes of companies due to external affect
            await gen.sleep(config.LOOP_UPDATE_TIME)

    def companies_changing(self, world_situation):
        cur_time = time.time()
        if cur_time- self.last_company_news_update >= config.COMPANY_NEWS_UPDATE:
            self.last_company_news_update = cur_time
            # Send world situation from news handler for a commit a progress of company
            self.companies_handler.commit_company_progress(world_situation)
            return
        
        if cur_time - self.last_company_cost_update >= config.COMPANY_COST_UPDATE:
            self.last_company_cost_update = cur_time
            self.companies_handler.recalculate_companies_stock_cost()
            return

    # Client request information about companies. Server return it
    def companies_open_list_client(self) -> list:
        return self.companies_handler.get_open_companies_to_list()

    # Client request to buy stock
    def request_to_buy_stock(self,uuid:str, amount : int, cost : float, client_data):
        return self.companies_handler.purchase_stock_of_comany(uuid,amount,cost,client_data)

    def request_to_sell_stock(self,uuid:str, amount: int, client_data):
        return self.companies_handler.sell_stock_of_company(uuid,amount,client_data)

    def request_news_list_bytime(self, time: float):
        return self.news_handler.get_news_list_bytime(time)

    def request_news_list_byamount(self, amount: int):
        return self.news_handler.get_news_list_byamount(amount)
