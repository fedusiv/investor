import uuid

from stock.stock_types import StockType
# Stock entity
# I suggest do not use here public variables. To be ensure, that it will somewhere by mistake changed
class Stock():

    @property
    def uuid(self):
        return self.__uuid

    @property
    def company_uuid(self):
        return self.__c_uuid

    # Value stored in real value. So if it is 12%, value should be 0.12
    @property
    def value(self):
        return self.__value

    @property
    def type(self):
        return self.__type

    @property
    def cost(self):
        return self.__cost

    # This property is used for SILVER type of stock
    # GOLD stock usually by default has owner when created
    @property
    def bought(self):
        return self.__bought

    @property
    def client_uuid(self):
        return self.__client_uuid

    @property
    def is_main(self):
        return self.__main

    # When inits it should return uuid of stock
    # c_uuid - company id, which stock belongs to
    # type - type of stock
    # value - what stock is a part of company value
    def __init__(self, c_uuid : str, type : StockType, value : float):
        self.__c_uuid = c_uuid
        self.__type = type
        self.__value = value

        # Generate unique id
        # TODO : check if it's good usage of uuid
        self.__uuid = str(uuid.uuid4())

        # Flag means, that stock is available to buy
        self.__bought = False
        # When player bought it, also better to store id of owner
        self.__client_uuid = ""
        # By default stock is not main
        self.__main = False

    # Main stock means, that player who owns it, he owns company and manage it. Or not server
    def set_as_main(self):
        self.__main = True

        # Calculate stock cost based on company value
    def calculate_cost(self, company_value : float):
        self.__cost = company_value * self.value

    # Set stock into bought state
    def buy_stock(self, client_uuid : str):
        self.__bought = True
        self.__client_uuid = client_uuid

    # Set stock into available state
    def sell_stock(self):
        self.__bought = True
        self.__client_uuid = ""

    # For debug
    def print_stock_data(self):
        print("uuid: ", self.uuid, "\tcompany uuid: ", self.company_uuid, "\tvalue: ", self.value, "\ttype", self.type, "\tcost: ", self.cost)


