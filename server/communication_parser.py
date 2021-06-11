from communication_protocol import CommunicationProtocol
from communication_protocol import MessageType
import utils

class CommunitcationParserResult():


    def __init__ (self, result_type = MessageType.NONE, success = True, uuid = ""):
        self.err = success
        self.result_type = result_type
        self.uuid = uuid
        self.result_type : MessageType

    def init_body(self, msg):
        self.msg_body = msg["body"]

    # For initialization client data
    # On login request it should store credentials, for futher parsing and validating
    def init_client_data(self, msg):
        self.login = msg["body"]["login"]
        self.password = msg["body"]["password"]
        try:
            if msg["body"]["admin"] == True:
                self.admin = True
        except:
            self.admin = False

    # To buy requested stock
    def form_stock_buy_request(self,msg):
        body = msg["body"]
        self.company_uuid = body["uuid"]	# what company want to buy
        self.stock_amount = body["amount"]	# amount of stocks want to buy
        self.stock_cost = 	body["cost"]	# what price of one stock was

    # To sell requested stock
    def form_stock_sell_request(self,msg):
        body = msg["body"]
        self.company_uuid = body["uuid"]	# what company want to sell
        self.stock_amount = body["amount"]	# amount of stocks want to sell

    # For history of 
    def form_history_request(self,msg):
        self.company_uuid = msg["body"]["uuid"]

    # Parsing parameters of news. by time and by amount
    def news_by_time(self,msg):
        self.news_time = msg["body"]["time"]
    def news_by_amount(self,msg):
        self.news_amount = msg["body"]["amount"]

    # Formulate request data to create 
    def create_company_data(self, msg):
        body = msg["body"]
        self.new_company_name : str = body["name"]
        self.b_type_int : int = body["b_type"]
        self.money_invest : float = body["money"]
        self.stocks_list = body["stocks"]

class CommunitcationParser():

    @staticmethod
    def keep_alive_respond(msg):
        utils.unused(msg)
        result = CommunitcationParserResult(MessageType.KEEP_ALIVE)
        return result

    @staticmethod
    def login_request(msg):
        result = CommunitcationParserResult(MessageType.LOGIN)
        result.init_client_data(msg)
        return result

    @staticmethod
    def registration_request(msg):
        print(CommunitcationParser.registration_request.__name__)
        result = CommunitcationParserResult(MessageType.REGISTRATION)
        result.init_client_data(msg)
        return result

    @staticmethod
    def companies_all_list_request(msg):
        result = CommunitcationParserResult(MessageType.COMPANIES_OPEN_LIST, uuid=msg["uuid"])
        return result

    @staticmethod
    def client_data_request(msg):
        result = CommunitcationParserResult(MessageType.CLIENT_DATA, uuid=msg["uuid"])
        return result

    @staticmethod
    def stock_buy_request(msg):
        result = CommunitcationParserResult(MessageType.BUY_STOCK, uuid=msg["uuid"])
        result.form_stock_buy_request(msg)
        return result

    @staticmethod
    def news_bytime_request(msg):
        result = CommunitcationParserResult(MessageType.NEWS_BY_TIME, uuid=msg["uuid"])
        result.news_by_time(msg)
        return result

    @staticmethod
    def news_byamount_request(msg):
        result = CommunitcationParserResult(MessageType.NEWS_BY_AMOUNT, uuid=msg["uuid"])
        result.news_by_amount(msg)
        return result

    @staticmethod
    def sell_silver_stock(msg):
        result = CommunitcationParserResult(MessageType.SELL_SILVER_STOCK, uuid=msg["uuid"])
        result.form_stock_sell_request(msg)
        return result

    @staticmethod
    def messaging(msg):
        result = CommunitcationParserResult(MessageType.MESSAGING,uuid=msg["uuid"])
        result.init_body(msg)
        return result

    @staticmethod
    def history_silver_stock(msg):
        result = CommunitcationParserResult(MessageType.COMPANY_SILVER_STOCK_HISTORY,uuid=msg["uuid"])
        result.form_history_request(msg)
        return result

    @staticmethod
    def create_player_company(msg):
        result = CommunitcationParserResult(MessageType.CREATE_PLAYER_COMPANY, uuid=msg["uuid"])
        result.create_company_data(msg)
        return result

    @staticmethod
    def parse_clinet_message(msg):
        # message should be json
        msg = CommunicationProtocol.verify_msg(msg)
        if msg is None:
            # end function is message is none
            return CommunitcationParserResult(False)

        switcher = {
            MessageType.LOGIN.value : CommunitcationParser.login_request,
            MessageType.REGISTRATION.value : CommunitcationParser.registration_request,
            MessageType.KEEP_ALIVE.value : CommunitcationParser.keep_alive_respond,
            MessageType.COMPANIES_OPEN_LIST.value : CommunitcationParser.companies_all_list_request,
            MessageType.CLIENT_DATA.value : CommunitcationParser.client_data_request,
            MessageType.BUY_STOCK.value : CommunitcationParser.stock_buy_request,
            MessageType.NEWS_BY_TIME.value : CommunitcationParser.news_bytime_request,
            MessageType.NEWS_BY_AMOUNT.value : CommunitcationParser.news_byamount_request,
            MessageType.SELL_SILVER_STOCK.value : CommunitcationParser.sell_silver_stock,
            MessageType.MESSAGING.value : CommunitcationParser.messaging,
            MessageType.COMPANY_SILVER_STOCK_HISTORY.value : CommunitcationParser.history_silver_stock,
            MessageType.CREATE_PLAYER_COMPANY.value : CommunitcationParser.create_player_company
        }
        # Verification is this admin message

        func = switcher.get(int(msg["type"]))
        result = func(msg)
        return result

