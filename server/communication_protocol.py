import json
from enum import Enum, unique

@unique
class MessageType(Enum):
    NONE = 0
    LOGIN = 1
    REGISTRATION = 2
    KEEP_ALIVE = 3
    COMPANIES_OPEN_LIST = 4
    BUY_STOCK = 5
    CLIENT_DATA = 6
    NEWS_BY_TIME = 7
    NEWS_BY_AMOUNT = 8
    SELL_SILVER_STOCK = 9
    MESSAGING = 10
    COMPANY_SILVER_STOCK_HISTORY = 11
    CREATE_PLAYER_COMPANY = 12
    WORKING_PLAN_REQUEST = 13

# Class to parse and create required messages
# This class used for server and client as well
class CommunicationProtocol():

    # Convert received message from json to required type and return in
    # if error return None
    @staticmethod
    def verify_msg(msg):
        # TODO there should be normal verification and deserialization. Also can be used custom class for deserialization
        message = json.loads(msg)
        return message

    @staticmethod
    def formulate_message(body,msg_type):
        msg = {"type" : msg_type,
            "body" : body}
        msg_json = json.dumps(msg)
        return msg_json

    # To client.
    @staticmethod
    def create_login_result_msg(result,uuid:str, msg = "", admin: bool = False):
        body = {
            "result" : result,
            "message" : msg,
            "uuid" : uuid,
            "admin" : admin
        }
        msg_json = CommunicationProtocol.formulate_message(body, MessageType.LOGIN.value)
        return msg_json

    @staticmethod
    def create_keep_alive_msg():
        body = {}
        msg_json = CommunicationProtocol.formulate_message(body, MessageType.KEEP_ALIVE.value)
        return msg_json

    # To client send list with all available open companies
    @staticmethod 
    def create_companies_open_list(c_list):
        if c_list is None:
            length = 0
            c_list = []
        else:
            length = len(c_list)
        body = {
            "amount" : length,
            "list" : c_list
        }
        msg_json = CommunicationProtocol.formulate_message(body, MessageType.COMPANIES_OPEN_LIST.value)
        return msg_json

    # To client, send client's data
    @staticmethod
    def create_client_data_msg(login : str, money : float, stock_list, server_time: float):
        s_list = {}
        if stock_list is not None:
            s_list = stock_list

        body = {
            "login" : login,
            "player_data":
            {
                "money" : money,
                "stocks" :
                {
                    "amount" : len(s_list),
                    "list" : s_list
                }
            },
            "server_time" : server_time
        }
        msg_json = CommunicationProtocol.formulate_message(body, MessageType.CLIENT_DATA.value)
        return msg_json

    # To client, send result of perchase
    @staticmethod
    def create_purchase_result(result : int):
        body = {
            "result" : result
        }
        msg_json = CommunicationProtocol.formulate_message(body, MessageType.BUY_STOCK.value)
        return msg_json

    # To client. create list of news. Happend from inserted amount of time
    @staticmethod
    def create_news_list(news_list):
        if news_list is None:
            length = 0
            news_list = []
        else:
            length = len(news_list)
        body = {
            "amount" : length,
            "news" : news_list
        }
        msg_json = CommunicationProtocol.formulate_message(body, MessageType.NEWS_BY_TIME.value)
        return msg_json

    @staticmethod
    def create_sell_result(result: int):
        body = {
            "result" : result
        }
        msg_json = CommunicationProtocol.formulate_message(body, MessageType.SELL_SILVER_STOCK.value)
        return msg_json

    @staticmethod
    def create_global_message(player_name : str, time, text:str):
        body = {
            "player_name" : player_name,
            "server_time" : time,
            "text" : text
        }
        msg_json = CommunicationProtocol.formulate_message(body, MessageType.MESSAGING.value)
        return msg_json

    @staticmethod
    def create_history_silver_stock(history_list):
        body = {
            "history" : history_list
        }
        msg_json = CommunicationProtocol.formulate_message(body, MessageType.COMPANY_SILVER_STOCK_HISTORY.value)
        return msg_json


    @staticmethod
    def create_company_result(result: int):
        body = {
            "result" : result
        }
        msg_json = CommunicationProtocol.formulate_message(body, MessageType.CREATE_PLAYER_COMPANY.value)
        return msg_json

    @staticmethod
    def working_plan_request_result(result):
        body = result
        msg_json = CommunicationProtocol.formulate_message(body, MessageType.WORKING_PLAN_REQUEST.value)
        return msg_json
