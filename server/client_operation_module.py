# This class operates logic of clients requests and actions
# Reason is to separate operation module from client connection module

import tornado.websocket

from communication_parser import CommunitcationParserResult
from companies.companies_types import CompanyCreateResult, CompanyWorkingRequestResult, StockSellResult
from investment.investment_types import InvestmentMakeResult, InvestmentPlanCreateResult, InvestmentType
from logic_handler import LogicHandler
from communication_protocol import MessageType
from communication_protocol import CommunicationProtocol
from client_data import ClientData
from companies.companies_handler import StockPurchaseResult
from investment.investment_market import InvestmentMarket
import utils

class ClientOperation():

    def __init__(self, ws : tornado.websocket.WebSocketHandler, logic_handler : LogicHandler):
        self.ws = ws
        self.logic_handler = logic_handler
        self.client_data : ClientData
        self.investment_market = InvestmentMarket.Instance()

    def parse_command(self,cmd : CommunitcationParserResult):
        switcher = {
            MessageType.COMPANIES_OPEN_LIST : self.request_open_companies_list,
            MessageType.CLIENT_DATA : self.request_client_data,
            MessageType.SHORT_INFO : self.short_client_data,
            MessageType.BUY_STOCK : self.request_to_buy_stock,
            MessageType.NEWS_BY_TIME : self.request_for_news_list_bytime,
            MessageType.NEWS_BY_AMOUNT : self.request_for_news_list_byamount,
            MessageType.SELL_SILVER_STOCK : self.request_to_sell_stock,
            MessageType.COMPANY_SILVER_STOCK_HISTORY : self.request_silver_stock_history,
            MessageType.CREATE_PLAYER_COMPANY : self.create_player_company_request,
            MessageType.WORKING_PLAN_REQUEST : self.request_working_plan_create,
            MessageType.WORKING_PLAN_APPLY : self.apply_working_plan,
            MessageType.INVEST_PLAN_CREATE : self.post_invest_plan,
            MessageType.INVEST_MARKET_LIST : self.list_invest_market,
            MessageType.INVEST_MAKE : self.investment_apply
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


    def short_client_data(self,cmd):
        utils.unused(cmd)
        player_data = self.client_data.player_data.get_player_value_info() # Money and stock's money
        news_list = self.logic_handler.news_handler.get_news_list_byamount(3)
        msg = CommunicationProtocol.prepare_short_info(self.client_data.login,
                                                        player_data,
                                                        self.logic_handler.server_time,
                                                        self.logic_handler.game_cycle,
                                                        news_list)
        self.ws.write_message(msg)

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

    def post_invest_plan(self, cmd: CommunitcationParserResult):
        # Verify, that company exists
        company = self.logic_handler.companies_handler.company_by_uuid(cmd.company_uuid)
        if company is None:
            msg = CommunicationProtocol.invest_plan_create_and_post(InvestmentPlanCreateResult.NO_SUCH_COMPANY.value)
            self.ws.write_message(msg)
            return
        # verify that player is owner
        player_uuid = company.owner_info[1]
        if player_uuid != self.client_data.uuid:
            msg = CommunicationProtocol.invest_plan_create_and_post(InvestmentPlanCreateResult.NOT_OWNER.value)
            self.ws.write_message(msg)
            return
        # Create plan object in investment Market
        plan = self.investment_market.create_and_post_investment_plan(server_time=self.logic_handler.server_time,
                                                                c_uuid=cmd.company_uuid,
                                                                c_name=company.name,
                                                                invest_value=cmd.invest_value,
                                                                i_type=cmd.invest_type,
                                                                payback_value=cmd.payback_value,
                                                                cycle_period=cmd.invest_cycles)
        # Append plan to pending list of investment plans
        company.invest_plan_append(plan)
        # send result
        msg = CommunicationProtocol.invest_plan_create_and_post(InvestmentPlanCreateResult.SUCCESS.value)
        self.ws.write_message(msg)

    def list_invest_market(self, cmd: CommunitcationParserResult):
        utils.unused(cmd)
        m_list = self.investment_market.list_of_investment_offers()
        msg = CommunicationProtocol.invest_market_list(m_list)
        self.ws.write(msg)

    # Player decided to make investment to a company. We can be only happy for that company.
    # Let's proceed with this functionality
    def investment_apply(self, cmd: CommunitcationParserResult):
        # First let's check if investment plan exists
        plan = self.investment_market.make_investment(cmd.investment_uuid)
        if plan is None:
            msg = CommunicationProtocol.investment_make_result(InvestmentMakeResult.NO_SUCH_INVESTMENT_PLAN.value)
            self.ws.write_message(msg)
            return
        # Verify, that company still exists
        company = self.logic_handler.companies_handler.company_by_uuid(plan.company_uuid)
        if company is None:
            msg = CommunicationProtocol.investment_make_result(InvestmentMakeResult.NO_SUCH_COMPANY.value)
            self.ws.write_message(msg)
            return
        # Verify that company has this investment plan as pending
        if company.invesment_plan_pending_existance_verify(plan) is False:
            msg = CommunicationProtocol.investment_make_result(InvestmentMakeResult.NO_PLAN_IN_COMPANY.value)
            self.ws.write_message(msg)
            return
        # After this applying functions go.

        # Verify, that player has enough money and remove them from player
        if self.client_data.player_data.make_investment(plan, self.logic_handler.game_cycle) is False:
            msg = CommunicationProtocol.investment_make_result(InvestmentMakeResult.NOT_ENOUGH_MONEY.value)
            self.ws.write_message(msg)
            return
        # Move investment to production state in company
        company.investment_apply(plan)
        # Set end cycle of investment plan

        # Send positive result to client
        msg = CommunicationProtocol.investment_make_result(InvestmentMakeResult.SUCCESS.value)
        self.ws.write_message(msg)
