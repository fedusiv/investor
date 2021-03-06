import time

from tornado import gen

from client.client_data import ClientData
from client.clients_handler_callback_type import ClientsHandlerCallbackType
from companies.companies_handler import CompaniesHandler
from news.news_handler import NewsHandler
from investment.investment_market import InvestmentMarket
from time_module import TimeModule
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
        self.time_module = TimeModule.Instance()
        self.investment_market = InvestmentMarket.Instance()
        # Time counters for companies update
        self.last_company_news_update = time.time()
        self.last_company_cost_update = time.time()
        # Cycle init. Cycle is game mechanics to represent life time and some logic
        self.game_cycle = 0
        self._cycle_ended = False

    # Connection between clients_handler and logic in opposite way is by callback
    def set_clients_handler_callback(self,func):
        self.clients_handler_callback = func
    #---------------------#
    #Properties part
    #---------------------#
    @property
    def server_time(self):
        return self.time_module.server_time

    #---------------------#
    #Logic part
    #---------------------#

    # Main loop of logic handler!
    async def logic_loop(self):
        self.time_module.start_mark()
        while True:
            # Calculate time
            self.time_module.tick()

            self.news_handler.update_news(self.server_time) # Call news main handler.
            self.companies_handler.update_companies() # Call companies main handler
            self.companies_changing(self.news_handler.world_situation) # Call changes of companies due to external affect
            await gen.sleep(config.LOOP_UPDATE_TIME)

    def companies_changing(self, world_situation):
        cur_time = self.server_time

        # This is end cycle operation
        if cur_time - self.last_company_news_update >= config.COMPANY_NEWS_UPDATE:
            self.last_company_news_update = cur_time
            # Increase game cycle. It should be dome in only one place
            self.game_cycle += 1
            # Send world situation from news handler for a commit a progress of company
            self.companies_handler.commit_company_progress(world_situation, cur_time, self.game_cycle)
            self._cycle_ended = True
            return

        # This is cycle begin operation
        if self._cycle_ended:
            self._cycle_ended = False
            self.investment_processing()

        # Probably unnecessary method, because company cost need to be updated each time after buying or selling it
        # And recalculation appears there
        if cur_time - self.last_company_cost_update >= config.COMPANY_COST_UPDATE:
            self.last_company_cost_update = cur_time
            self.companies_handler.recalculate_companies_stock_cost(cur_time)
            return

    def investment_processing(self):
        investors_data_list = self.companies_handler.get_expiring_investment_contracts_payment(self.game_cycle)
        # investors_data_list item representation, taken from function above
        #"player_uuid" : contract.player_uuid
        #"debt" : debt,
        #"contract" : contract_uuid
        # First need to send money to connected players
        if self.clients_handler_callback is None:
            print("Callback is none")
            return
        for item in investors_data_list:
           self.clients_handler_callback(ClientsHandlerCallbackType.SEND_INVEST_MONEY,item)
        # TODO: add to proceed with disconnected clients

    # Client request information about companies. Server return it
    def companies_open_list_client(self) -> list:
        return self.companies_handler.get_open_companies_to_list()

    # Client request to buy stock
    def request_to_buy_stock(self,uuid:str, amount : int, client_data: ClientData):
        return self.companies_handler.purchase_stock_of_comany(uuid,amount,client_data.player_data)

    def request_to_sell_stock(self,uuid:str, amount: int, client_data: ClientData):
        return self.companies_handler.sell_stock_of_company(uuid,amount,client_data.player_data)

    def request_news_list_bytime(self, time: float):
        return self.news_handler.get_news_list_bytime(time)

    def request_news_list_byamount(self, amount: int):
        return self.news_handler.get_news_list_byamount(amount)

    def request_siler_stock_history(self,company_uuid: str):
        return self.companies_handler.get_silver_stocks_history(company_uuid)

    def request_to_create_closed_company(self, company_name:str, b_type: int, money: float, stocks: list, client_data: ClientData):
        return self.companies_handler.create_closed_company(company_name=company_name,
                                                            b_type=b_type,
                                                            money=money,
                                                            stocks=stocks,
                                                            player_data=client_data.player_data)

    def request_working_plan_create(self, c_uuid: str, begin_cycle: int, end_cycle: int, target:float):
        return self.companies_handler.create_working_plan_request(c_uuid=c_uuid,
                                                                begin_cycle=begin_cycle,
                                                                end_cycle=end_cycle,
                                                                target=target,
                                                                w_sit=self.news_handler.world_situation)

    def request_working_plan_apply(self, c_uuid: str, w_uuid: str):
        return self.companies_handler.working_plan_apply(c_uuid, w_uuid)

    def request_companies_name_list(self):
        return self.companies_handler.get_companies_id_to_list()
