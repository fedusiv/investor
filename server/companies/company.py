import random
import time
from uuid import uuid4

from companies.companies_types import CompanyType
from companies.companies_types import CompanyBusinessType
from companies.company_data import CompanyData
from companies.company_name_generation import CompanyNameGenerator
from stock.stock import Stock
from stock.stock import StockType
from companies.bussines_news_connection import BusinessNewsRelation, NewsDependency
from news.world_situation import WorldSituation
import config
import utils

# Operate with company
class Company():

    @property
    def name(self):
        return self.data.name
    @property
    def uuid(self):
        return self.data.uuid
    @property
    def value(self):
        return self.data.value

    @property
    def silver_cost(self) -> float:
        for stock in self.stocks.values():
            stock : Stock
            if stock.type != StockType.SILVER:
                continue
            # itarate loop until we received first Silver stock
            if stock.cost <= 0:
                continue
            else:
                return stock.cost
        # Something can happend and return value will be nothing need to return 0
        # Or if company is CLOSED there is no silver stocks, so need to return 0
        return 0.0

    @property
    def silver_full_amount(self):
        return self.__silver_amount_full

    @property
    def silver_available_amount(self):
        return self.__silver_amount_full - self.__silver_amount_bought

    @property
    def gold_full_amount(self):
        return self.__gold_amount_full

    @property
    def value_rate(self):
        return self.__value_rate

    @property
    def owner_info(self):
        return self.__owner_name, self.__owner_uuid

    # Init generates default random Company 
    def __init__(self):
        # Dictionary for stocks. Storage.
        # {stock_uuid : stock_object}
        self.stocks = {}

        # Create data object
        self.data = CompanyData()
        # Generate uniq id.
        # TODO : verify, that this is right solution
        self.data.uuid = str(uuid4())
        # On init stage company has none type and can't participate on marketing operations
        # Assume that type will be changed further
        self.company_type = CompanyType.NONE

        self.__silver_amount_full = 0 # Amount of stocks
        self.__silver_amount_bought = 0 # Amount of stocks which are bought

        self.__gold_amount_full = 0 # Amount of gold stocks
        # Rise value, company if works will increase own value
        self.__value_rate = 1.0
        # By default compane has zero influence level
        self.influence_level = 0
        # Counter for world damping news situation.
        # If even after damping amount, company has same influence_stage level
        #   so means, need to increase default value rate for this influence level
        self.current_world_damping = 0

        # History of silver stock changing prices
        self.silver_stock_history = {}

        # owner information
        self.__owner_name = "" # empty name means server is owner
        self.__owner_uuid = "a1" # a1 means server is owner of company

    def set_company_name(self, name: str):
        self.data.name = name

    def generate_random_name(self):
       # Generate name
        self.data.name = CompanyNameGenerator.name_generate()

    def apply_company_new_business_type(self, b_type: int):
        self.business_type : CompanyBusinessType = CompanyBusinessType(b_type)
        self.news_dependency : NewsDependency = BusinessNewsRelation.business_news_relation(self.business_type)

    # Set to company random business type and apply news dependence
    def generate_random_company_type(self):
        # Generate type
        random.seed(time.time())
        self.business_type : CompanyBusinessType = random.choice(list(CompanyBusinessType))
        self.news_dependency : NewsDependency = BusinessNewsRelation.business_news_relation(self.business_type)

    def generate_open_company_random_value(self):
        random.seed(time.time())
        random_cost = random.uniform(15000.0, 50000.0)
        self.data.value = round(random_cost,2)


    def generate_closed_company_random_value(self):
        random.seed(time.time())
        random_cost = random.uniform(2000.0, 6000.0)
        self.data.value = round(random_cost,2)

    # Probably temporaty method
    # Generate 1 gold stock with 51% of value. And other of 49% with given amount
    # So full amount is 1 GOLD + amount of SILVER
    def generate_stocks51(self, amount: int):
        # Change type to open. This is kind of default stocks initialization
        self.company_type = CompanyType.OPEN
        # Create stocks
        main_stock = Stock(self.uuid, StockType.GOLD, 0.51)
        main_stock.set_as_main()
        self.stocks[main_stock.uuid] = main_stock
        self.__gold_amount_full += 1
        # Generate others
        value = (49 / amount) / 100
        for _unused in range(0,amount):
            utils.unused(_unused)
            stock = Stock(self.uuid, StockType.SILVER, value)
            self.stocks[stock.uuid] = stock
            self.__silver_amount_full += 1
        # After generation need to calculate stock cost
        self.recalculate_stocks_cost()

    # Default generator stocks for closed type companies
    def generate_closed_stocks(self):
        # Set type to closed
        self.company_type = CompanyType.CLOSED
        # Generate main stock
        main_stock = Stock(self.uuid, StockType.GOLD, 0.51)
        main_stock.set_as_main()
        self.stocks[main_stock.uuid] = main_stock
        self.__gold_amount_full +=1
        # Next decided, what amount of all generated stocks
        amount = random.randint(3,7)
        # Available stock percentage
        persentage = 0.49
        for i in range(0,amount-1):
            random.seed(time.time())
            limit_a = round(persentage/(amount - i),2)
            limit_b = round(persentage/2,2) # maximum it can be a half of available persentage
            cur_persentage = round(random.uniform(limit_a,limit_b))
            # Create stock
            persentage -= cur_persentage
            stock = Stock(self.uuid, StockType.GOLD, cur_persentage) # Create stock
            self.stocks[stock.uuid] = stock # Store
            self.__gold_amount_full +=1

        # Loop goes amount-1, that means one left to store all persentage that left
        stock = Stock(self.uuid, StockType.GOLD, persentage) # Create stock
        self.stocks[stock.uuid] = stock
        self.__gold_amount_full +=1
        # Recalculation after generation
        self.recalculate_stocks_cost()

    # Create! gold stocks for the company
    # stock_list - list of float value, which amount stock will have
    def create_gold_stocks(self, stock_list : list, client_uuid : str):
        stocks_created = [] # reference of created stocks to attach them to owner
        # get maximum value of stock_list to set it as main stock. Flag, that represent who can manage company
        max_value = max(stock_list)
        max_stock_applied = False
        for amount in stock_list:
            stock = Stock(self.uuid, StockType.GOLD, amount)
            if (amount == max_value) and (max_stock_applied is False):
                # TODO: Create mechanism to check, that only one stock in company is main
                # Set main stock
                stock.set_as_main()
            stock.buy_stock(client_uuid)
            self.stocks[stock.uuid] = stock
            self.__gold_amount_full += 1
            stocks_created.append(stock)
        self.recalculate_stocks_cost()
        return stocks_created

    # Set company value rate as multiplier to current value
    def set_rate_value(self, value_rate : float):
        self.__value_rate = value_rate

    # Increase company value based on current rate
    def increase_value_by_rate(self):
        self.data.value = self.data.value * self.value_rate

    # Increase value of company, when money were invested to it
    def increase_value(self, money: float):
        self.data.value += money

    # When company change it's value, better to recalculate stocks cost
    def recalculate_stocks_cost(self, server_time = 0.0):
        for stock in self.stocks.values():
            stock.calculate_cost(self.value)
        self.store_silver_stock_history(server_time)

    # Stores the history of silver stocks changes
    def store_silver_stock_history(self,time = 0.0):
        if time == 0.0:
            # Time is not set, no need to store in history
            return
        self.silver_stock_history[time] = self.silver_cost

    def get_silver_stock_history(self):
        history = []
        for key in self.silver_stock_history.keys():
            el = { key : self.silver_stock_history[key] }
            history.append(el)
        return history

    # Changing value rate of company based on world situation
    def change_value_due_worldsituation(self,situation : WorldSituation):
        rate = 0.0
        inf_level = situation.required_influence_types_level(self.news_dependency)

        # Depends on influence level of current world situation, choose rate for current update
        # TODO: Need to move this table to some kind of config values, and do not keep it as hardcoded constant representation
        rate_switcher = {
            1 : 0.03,
            2: 0.07,
            3: 0.15,
            4: 0.21,
            5: 0.25,
            6: 0.32
        }
        rate = rate_switcher.get(abs(inf_level), 0.0)
        if inf_level < 0:
            rate = -1 * rate

        new_rate = self.value_rate_progression(rate, inf_level)
        self.set_rate_value(new_rate)

    # If copmany received same influence stage even after damping amount
    #   so in this case value rate should be increased
    def value_rate_progression(self, rate: float, inf_level : int) -> float:
        if self.influence_level == inf_level:
            if self.influence_level == 0:
                # Some kind of stagnation, let's make some smooth random value to fill changes anyway
                random.seed(time.time())
                rate = random.uniform(-0.011,0.011)
                rate = round(rate,3)
            else:
            # Otherwise increasing rate for not NONE influence
                # Current influence stage is equal to given influence stage.
                self.current_world_damping += 1
                if self.current_world_damping > config.NEWS_DAMPING_AMOUNT:
                    # if damping is bigger so rate should be increased
                    rate = rate * 1.75
                    self.current_world_damping = 0 # Clear counter
        else:
            # if level is different. set current level to received influence stage
            self.influence_level = inf_level
            self.current_world_damping = 0 # Clear counter
        # Rate value always 
        value = 1 + rate
        return value

    # Mechanism of changing company values
    # Server keep track of values at the beginning of cycle and use value rate at the end
    # Calculate the amount of money which company loose or earn in this cycle based on value with which is started
    # This mechanism makes companies even to bad world situation if there was huge amount of money invested,
    #   companies will anyway get some positive amount of value
    def cycle_end_recalculation(self):
        # Calculate the value, which depence only on news and world situation
        fake_value = self.data.cycle_start_value * self.value_rate
        difference = fake_value - self.data.cycle_start_value
        self.increase_value(difference)
        # And store the value for the new beginning of cycle
        self.data.cycle_start_value = self.value


    # Companies handler calls this method.
    # Company return list of stock, that will be bought
    def purchase_silver_stock(self, amount: int, client_uuid : str) -> list:
        stock_list = []
        counter = amount
        for stock in self.stocks.values():
            stock : Stock
            if stock.type == StockType.GOLD:
                continue	# not silver go next
            if stock.bought:
                continue	# already bought go next
            counter -= 1
            stock_list.append(stock)
            stock.buy_stock(client_uuid)
            self.__silver_amount_bought += 1

            if counter <= 0:
                break

        return stock_list

    # prepare dict of open company data
    # Open company should return information about silver stocks
    def prepare_open_company_data(self):
        # Send float only with 4 digits after comma
        cost = format(self.silver_cost,'.4f')
        data = {
            'uuid' : self.uuid,
            'name' : self.name,
            'cost' : cost,
            'b_type' : self.business_type.name
        }
        return data

    #############################
    # Server debug methods filed
    #############################

    def print_company_data(self):
        print("Company name: ", self.name)
        print("\tuuid: ", self.uuid, "\tvalue: ", self.value)
        print("\tstocks:")
        print(len(self.stocks))
        for stockey in self.stocks.keys():
            print("\t",end='',flush=True)
            self.stocks[stockey].print_stock_data()

    # Server debug method
    def print_company_values(self):
        print("Company name: ", self.name, "\tvalue: ", self.value, "\tvalue rate: ", self.value_rate, "\tsilver cost: ", self.silver_cost)
