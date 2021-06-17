import random
import time
from uuid import uuid4

from companies.companies_types import CompanyType
from companies.companies_types import CompanyBusinessType
from companies.company_data import CompanyData
from companies.company_name_generation import CompanyNameGenerator
from companies.working_plan import CompanyWorkingPlan
from investment.investment_plan import InvestmentPlan
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
    def fund_value(self):
        return self.data.fund_value

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
    def __init__(self, start_cycle_count: int):
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
        # Fund rate, what part of stocks income go to company value
        self.__fund_rate = 0.0
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

        # Life cycle information. Represent how many logic cycles company exists
        self.__life_cycle = 0
        # On what game cycle company was created
        self.__create_cycle = start_cycle_count

        # Working plans list
        self.__working_plans = []

        #Investment plans, which were requested by owner and await to be applied
        self._investment_plans_pending = []
        self._investment_plans_applied = []

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

    # Increase value of company, when money were invested to it
    def increase_value(self, money: float):
        # make changes in investments
        # Investment does not care where money goes to fund or to company value.
        self.investment_processing(money)
        if money >= 0:
            # Positive operations proceed through the fund of company
            fund_money = money * self.__fund_rate
            # Place them to company's fund
            self.data.fund_value += fund_money
            # Decrease amount of all income
            money -= fund_money
        # Put money to company value
        self.data.value += money

    # Change the value of company fund
    def increase_fund_value(self,money: float):
        self.data.fund_value += money

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

    # Closed companies aka player's company less depence on positive news and world situation
    # Rate need to be decreased
    def decrease_rate_for_closed_company(self):
        rate = self.__value_rate - 1
        new_rate = rate * config.CLOSED_COMPANY_RATE_DECREASE
        self.set_rate_value(new_rate)

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
    def cycle_end_recalculation(self, next_cycle: int):
        # Calculate the value, which depence only on news and world situation
        fake_value = self.data.cycle_start_value * self.value_rate
        difference = fake_value - self.data.cycle_start_value
        self.increase_value(difference)
        # Process with working plan changes
        if self.company_type == CompanyType.CLOSED:
            # Works with Closed companies
            # Open companies changes values only based on news
            self.working_plan_commit(next_cycle)
        # And store the value for the new beginning of cycle
        self.data.cycle_start_value = self.value
        # Go to next cycle
        self.__life_cycle = next_cycle - self.__create_cycle

     # Commit process of company related to working plan
    def working_plan_commit(self, next_cycle: int):
        cur_cycle = next_cycle - 1
        # Currently working plan is related only to closed companies
        if self.company_type == CompanyType.OPEN:
            return
        for plan in self.__working_plans:
            plan : CompanyWorkingPlan
            # Additional verification, to operate only applied with working plan
            if plan.applied is False:
                continue
            if plan.end_cycle == cur_cycle - 1:
                # Now is end of working plan, apply changes
                if self.data.value >= plan.end_value:
                    # Additional earn goes to fund first
                    self.increase_fund_value(plan.earn_value)
                else:
                    # if lose some money, it decrease company value, not fund
                    self.increase_value(-1 * plan.lose_value)
                # Working plan was applied, remove it from list
                self.__working_plans.remove(plan)
                # Only one working plan should be in a company in on period. Can exit now
                return
            else:
                # Need to understand does company have any working plan, that is running now, and no need to fine it
                if (plan.start_cycle <= cur_cycle) and (plan.end_cycle > cur_cycle):
                    return
        # Once received this line of code, means, that there is no working plan applied and running for company
        # Apply fine for it
        fine = 1 * config.WORKING_PLAN_FINE * self.__life_cycle
        self.increase_value(fine)



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

    # Just append working plan. Need tp store it somewhere
    def working_plan_append_pending(self, working_plan: CompanyWorkingPlan):
        self.__working_plans.append(working_plan)

    # Apply working plan
    def working_plan_apply(self, plan_uuid: str):
        # Verify, that plan exists
        cur_plan = None
        for plan in self.__working_plans:
            plan: CompanyWorkingPlan
            if plan.applied:
                continue
            if plan.plan_uuid == plan_uuid:
                cur_plan = plan
                break
        if cur_plan == None:
            return False
        if not self.working_verify_cycles(cur_plan.start_cycle,cur_plan.end_cycle) :
            return False
       # Apply working plan
        cur_plan.applied = True
        # Remove all pending plans
        for plan in self.__working_plans:
            plan: CompanyWorkingPlan
            if plan.applied is False:
                self.__working_plans.remove(plan)
        return True

    # verify, that given cycles are avalible
    def working_verify_cycles(self, begin_cycle: int, end_cycle: int):
        taken_cycles = []
        for plan in self.__working_plans:
            plan : CompanyWorkingPlan
            if plan.applied is False:
                continue
            # Fill taken cycles
            taken_cycles.append(plan.start_cycle)
            taken_cycles.append(plan.end_cycle)
        # Check that required cycles are not taken
        if begin_cycle in taken_cycles:
            return False
        if end_cycle in taken_cycles:
            return False
        return True

    # Method add invest plan to list of pending plans
    def invest_plan_append(self, plan):
        self._investment_plans_pending.append(plan)

    def invesment_plan_pending_existance_verify(self,plan):
        for element in self._investment_plans_pending:
            element: InvestmentPlan
            if plan == element:
                return True
        return False

    def investment_apply(self,plan: InvestmentPlan):
        # Remove from pending list
        self._investment_plans_pending.remove(plan)
        # Add to applied list
        self._investment_plans_applied.append(plan)
        # Increase fund
        self.increase_fund_value(plan.investment_value)

    def investment_processing(self, money: float):
        for element in self._investment_plans_applied:
            element: InvestmentPlan
            # Change amount of value, that company received since it was applied
            element.earn_value += money

    def investment_expiring_list(self, cur_cycle: int):
        c_list = []
        for contract in self._investment_plans_applied:
            contract : InvestmentPlan
            if contract.end_cycle == 0:
                continue
            elif contract.end_cycle <= cur_cycle:
                c_list.append(contract)
        return c_list

    # Expired contracts need to be removed from applied investment contracts
    def invesments_remove(self, contracts_list):
        for contract in contracts_list:
            if contract in self._investment_plans_applied:
                self._investment_plans_applied.remove(contract)

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
