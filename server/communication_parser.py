from client_data import ClientData
from communication_protocol import CommunicationProtocol
from communication_protocol import MessageType


class CommunitcationParserResult():


    def __init__ (self, result_type = MessageType.NONE, success = True, uuid = ""):
        self.err = success
        self.result_type = result_type
        self.uuid = uuid
        self.result_type : MessageType

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


    # Parsing parameters of news. by time and by amount
    def news_by_time(self,msg):
        self.news_time = msg["body"]["time"]
    def news_by_amount(self,msg):
        self.news_amount = msg["body"]["amount"]


class CommunitcationParser():

    @staticmethod
    def keep_alive_respond(msg):
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
            MessageType.SELL_SILVER_STOCK.value : CommunitcationParser.sell_silver_stock
        }
        # Verification is this admin message

        func = switcher.get(int(msg["type"]))
        result = func(msg)
        return result

