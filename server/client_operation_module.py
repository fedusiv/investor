# This class operates logic of clients requests and actions
# Reason is to separate operation module from client connection module

import tornado.websocket

from communication_parser import CommunitcationParserResult
from companies.companies_types import CompanyCreateResult, CompanyWorkingRequestResult, StockSellResult
from logic_handler import LogicHandler
from communication_protocol import MessageType
from communication_protocol import CommunicationProtocol
from client_data import ClientData
from companies.companies_handler import StockPurchaseResult
import utils

class ClientOperation():

    def __init__(self, ws : tornado.websocket.WebSocketHandler, logic_handler : LogicHandler):
        self.ws = ws
        self.logic_handler = logic_handler
        self.client_data : ClientData

    def parse_command(self,cmd : CommunitcationParserResult):
        switcher = {
            MessageType.COMPANIES_OPEN_LIST : self.request_open_companies_list,
            MessageType.CLIENT_DATA : self.request_client_data,
            MessageType.BUY_STOCK : self.request_to_buy_stock,
            MessageType.NEWS_BY_TIME : self.request_for_news_list_bytime,
            MessageType.NEWS_BY_AMOUNT : self.request_for_news_list_byamount,
            MessageType.SELL_SILVER_STOCK : self.request_to_sell_stock,
            MessageType.COMPANY_SILVER_STOCK_HISTORY : self.request_silver_stock_history,
            MessageType.CREATE_PLAYER_COMPANY : self.create_player_company_request,
            MessageType.WORKING_PLAN_REQUEST : self.request_working_plan_create,
            MessageType.WORKING_PLAN_APPLY : self.apply_working_plan
        }
        func = switcher.get(cmd.result_type)
        func(cmd)

    def wrong_command(self,cmd):
        utils.unused(cmd)
        print("Wrong type")

    def request_open_companies_list(self,cmd):
        utils.unused(cmd)
        c_list = self.logic_handler.companies_open_list_client()
        c_list_msg = CommunicationProtocol.create_companies_open_list(c_list)
        self.ws.write_message(c_list_msg)

    # Send to client, client's data
    def request_client_data(self,cmd):
        utils.unused(cmd)
        s_list = self.client_data.player_data.get_all_stocks_to_list()
        client_data_msg = CommunicationProtocol.create_client_data_msg(login= self.client_data.login,
                                                                        money=self.client_data.player_data.money,
                                                                        stock_list=s_list,
                                                                        server_time=self.logic_handler.server_time)
        self.ws.write_message(client_data_msg)

    # Client send request to buy a stock
    def request_to_buy_stock(self,cmd : CommunitcationParserResult):
        result : StockPurchaseResult
        result = self.logic_handler.request_to_buy_stock(cmd.company_uuid,cmd.stock_amount, cmd.stock_cost, self.client_data)
        result_msg = CommunicationProtocol.create_purchase_result(result.value)
        self.ws.write_message(result_msg)

    def request_to_sell_stock(self, cmd: CommunitcationParserResult):
        result : StockSellResult
        result = self.logic_handler.request_to_sell_stock(cmd.company_uuid, cmd.stock_amount, self.client_data)
        result_msg = CommunicationProtocol.create_sell_result(result.value)
        self.ws.write_message(result_msg)

    def request_for_news_list_bytime(self, cmd : CommunitcationParserResult):
        news_list = self.logic_handler.request_news_list_bytime(cmd.news_time)
        news_list_msg = CommunicationProtocol.create_news_list(news_list)
        self.ws.write_message(news_list_msg)

    def request_for_news_list_byamount(self, cmd : CommunitcationParserResult):
        news_list = self.logic_handler.request_news_list_byamount(cmd.news_amount)
        news_list_msg = CommunicationProtocol.create_news_list(news_list)
        self.ws.write_message(news_list_msg)

    def request_silver_stock_history(self, cmd : CommunitcationParserResult):
        history_list = self.logic_handler.companies_handler.get_silver_stocks_history(cmd.company_uuid)
        history_list_msg = CommunicationProtocol.create_history_silver_stock(history_list)
        self.ws.write_message(history_list_msg)

    def create_player_company_request(self, cmd: CommunitcationParserResult):
        result : CompanyCreateResult
        result = self.logic_handler.request_to_create_closed_company(company_name=cmd.new_company_name,
                                                                    b_type=cmd.b_type_int,
                                                                    money=cmd.money_invest,
                                                                    stocks=cmd.stocks_list,
                                                                    client_data=self.client_data)
       # Send result message
        create_company_msg = CommunicationProtocol.create_company_result(result.value)
        self.ws.write_message(create_company_msg)

    def request_working_plan_create(self, cmd : CommunitcationParserResult):
        result = self.logic_handler.request_working_plan_create(c_uuid=cmd.company_uuid,
                                                                    begin_cycle=cmd.begin_cycle,
                                                                    end_cycle=cmd.end_cycle,
                                                                    target=cmd.target_earn)
        plan_request = CommunicationProtocol.working_plan_request_result(result)
        self.ws.write_message(plan_request)

    def apply_working_plan(self, cmd : CommunitcationParserResult):
        result : CompanyWorkingRequestResult
        result = self.logic_handler.request_working_plan_apply(cmd.company_uuid, cmd.w_plan_uuid)
        msg = CommunicationProtocol.working_plan_apply(result.value)
        self.ws.write(msg)
