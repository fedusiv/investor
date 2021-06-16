from communication_protocol import CommunicationProtocol
from communication_protocol import MessageType
import utils

class CommunitcationParserResult():


    def __init__ (self,msg, result_type = MessageType.NONE, success = True):
        self.err = success
        self.result_type = result_type
        self.uuid = msg["uuid"]
        self.result_type : MessageType
        self.body = msg["body"]

    # For initialization client data
    # On login request it should store credentials, for futher parsing and validating
    def init_client_data(self):
        self.login = self.body["login"]
        self.password = self.body["password"]
        try:
            if self.body["admin"] == True:
                self.admin = True
        except:
            self.admin = False

    # To buy requested stock
    def form_stock_buy_request(self):
        self.company_uuid = self.body["uuid"]	# what company want to buy
        self.stock_amount = self.body["amount"]	# amount of stocks want to buy
        self.stock_cost =   self.body["cost"]	# what price of one stock was

    # To sell requested stock
    def form_stock_sell_request(self):
        self.company_uuid = self.body["uuid"]	# what company want to sell
        self.stock_amount = self.body["amount"]	# amount of stocks want to sell

    # For history of 
    def form_history_request(self):
        self.company_uuid = self.body["uuid"]

    # Parsing parameters of news. by time and by amount
    def news_by_time(self):
        self.news_time = self.body["time"]
    def news_by_amount(self):
        self.news_amount = self.body["amount"]

    # Formulate request data to create 
    def create_company_data(self):
        self.new_company_name : str = self.body["name"]
        self.b_type_int : int = self.body["b_type"]
        self.money_invest : float = self.body["money"]
        self.stocks_list = self.body["stocks"]

    def create_working_request(self):
        self.company_uuid = self.body["uuid"]
        self.begin_cycle = self.body["begin_cycle"]
        self.end_cycle = self.body["end_cycle"]
        self.target_earn = self.body["target"]

    def working_plan_apply(self):
        self.company_uuid = self.body["c_uuid"]
        self.w_plan_uuid = self.body["w_uuid"]

class CommunitcationParser():

    @staticmethod
    def keep_alive_respond(msg):
        utils.unused(msg)
        result = CommunitcationParserResult(msg,MessageType.KEEP_ALIVE)
        return result

    @staticmethod
    def login_request(msg):
        result = CommunitcationParserResult(msg,MessageType.LOGIN)
        result.init_client_data()
        return result

    @staticmethod
    def registration_request(msg):
        print(CommunitcationParser.registration_request.__name__)
        result = CommunitcationParserResult(msg,MessageType.REGISTRATION)
        result.init_client_data()
        return result

    @staticmethod
    def companies_all_list_request(msg):
        result = CommunitcationParserResult(msg,MessageType.COMPANIES_OPEN_LIST)
        return result

    @staticmethod
    def client_data_request(msg):
        result = CommunitcationParserResult(msg,MessageType.CLIENT_DATA)
        return result

    @staticmethod
    def short_info_request(msg):
        result = CommunitcationParserResult(msg,MessageType.SHORT_INFO)
        return result

    @staticmethod
    def stock_buy_request(msg):
        result = CommunitcationParserResult(msg,MessageType.BUY_STOCK)
        result.form_stock_buy_request()
        return result

    @staticmethod
    def news_bytime_request(msg):
        result = CommunitcationParserResult(msg,MessageType.NEWS_BY_TIME)
        result.news_by_time()
        return result

    @staticmethod
    def news_byamount_request(msg):
        result = CommunitcationParserResult(msg,MessageType.NEWS_BY_AMOUNT)
        result.news_by_amount()
        return result

    @staticmethod
    def sell_silver_stock(msg):
        result = CommunitcationParserResult(msg,MessageType.SELL_SILVER_STOCK)
        result.form_stock_sell_request()
        return result

    @staticmethod
    def messaging(msg):
        result = CommunitcationParserResult(msg,MessageType.MESSAGING)
        return result

    @staticmethod
    def history_silver_stock(msg):
        result = CommunitcationParserResult(msg,MessageType.COMPANY_SILVER_STOCK_HISTORY)
        result.form_history_request()
        return result

    @staticmethod
    def create_player_company(msg):
        result = CommunitcationParserResult(msg,MessageType.CREATE_PLAYER_COMPANY)
        result.create_company_data()
        return result

    @staticmethod
    def request_working_plan(msg):
        result = CommunitcationParserResult(msg,MessageType.WORKING_PLAN_REQUEST)
        result.create_company_data()
        return result

    @staticmethod
    def apply_working_plan(msg):
        result = CommunitcationParserResult(msg, MessageType.WORKING_PLAN_APPLY)
        result.working_plan_apply()
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
            MessageType.CREATE_PLAYER_COMPANY.value : CommunitcationParser.create_player_company,
            MessageType.WORKING_PLAN_REQUEST.value : CommunitcationParser.request_working_plan,
            MessageType.WORKING_PLAN_APPLY.value : CommunitcationParser.apply_working_plan,
            MessageType.SHORT_INFO.value : CommunitcationParser.short_info_request
        }
        # Verification is this admin message

        func = switcher.get(int(msg["type"]))
        result = func(msg)
        return result

