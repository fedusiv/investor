from typing import TypedDict
import math


from companies.company import Company
from companies.companies_types import CompanyBusinessType, CompanyCreateResult, CompanyType, CompanyWorkingRequestResult, StockSellResult
from companies.companies_types import StockPurchaseResult
from client_data import ClientData
from companies.working_plan import CompanyWorkingPlan
import config
from investment.investment_plan import InvestmentPlan
import utils
from news.world_situation import WorldSituation

# Storage class. I hope this will make some improvement to storage mechanism
# At least autocompletion works fine
class CompanyStorageElement(TypedDict):
    uuid : str
    company : Company

# Singleton respond for all companies movement and operations
class CompaniesHandler():
    # Singleton part
    __instance = None
    @staticmethod

    def Instance():
        if CompaniesHandler.__instance == None:
            CompaniesHandler()
        return CompaniesHandler.__instance

    def __init__(self):
        CompaniesHandler.__instance = self
        # Company storage. List of CompanyStorageElement. Probably in the future maybe need to implement a custom class for storage
        # for easier operations with it
        self.__companies_storage = []
        self.__amount_open_companies = 0
        self.__amount_closed_companies = 0
        # Represent current game cycle
        self.game_cycle = 0

    #---------------------#
    #Logic part
    #---------------------#

    # Get company by it's uuid
    def company_by_uuid(self, uuid: str)-> Company:
        company = None
        for element in self.__companies_storage:
            element : CompanyStorageElement
            if element['uuid'] == uuid:
                company = element['company']
                break
        return company


    # Main loop of companies handler. It is called from logic handler
    def update_companies(self):
        # Update companies amount. If some company disappeared need to replace it
        self.update_companies_amount()

    # Check current companies amount, if less create new
    def update_companies_amount(self):
        while self.__amount_open_companies < config.MAX_OPEN_COMPANIES_AMOUNT:
            self.generate_open_company()

    def generate_open_company(self):
        # Create companies
        new_company = Company(self.game_cycle)
        new_company.generate_random_name() # Apply random name
        new_company.generate_random_company_type() # Apply random business type
        new_company.generate_open_company_random_value() # Set random value for company
        # Generate default set of stocks for open company
        new_company.generate_stocks51(config.OPEN_COMPANY_DEFAULT_AMOUNT_SILVER_STOCKS)
        element = CompanyStorageElement(uuid=new_company.uuid,company=new_company)
        self.__amount_open_companies += 1
        self.__companies_storage.append(element)

    # Kind a random generation process of closed company
    def generate_closed_company(self):
        # Create companies
        new_company = Company(self.game_cycle)
        new_company.generate_closed_company_random_value()
        # Generate default set of stocks for closed company
        new_company.generate_closed_stocks()
        element = CompanyStorageElement(uuid=new_company.uuid,company=new_company)
        self.__amount_closed_companies += 1
        self.__companies_storage.append(element)

    # Player's request to create closed company
    def create_closed_company(self, company_name:str, b_type: int, money: float, stocks: list, client_data: ClientData) -> CompanyCreateResult:
        # Verify that name is ok, and there is no already same name
        if not self.verify_syntax_new_company_name(company_name):
            return CompanyCreateResult.NAME_SYNTAX_ERROR
        if not self.verify_uniq_new_company_name(company_name):
            return CompanyCreateResult.NAME_NOT_UNIQ
        # Next verification about company type
        if not self.verify_business_type_existance(b_type):
            return CompanyCreateResult.B_TYPE_ERROR
        # Verify stocks proper devision
        for value in stocks:
            if value < config.MINIMUN_STOCK_VALUE_TO_CREATE:
                return CompanyCreateResult.STOCKS_ERROR
        stocks_sum = sum(stocks)
        if stocks_sum != 100:
            return CompanyCreateResult.STOCKS_ERROR

        # All verification steps are done. Here company can be created
        new_company = Company(self.game_cycle)
        # This is closed company, means only have private own stocks
        new_company.company_type = CompanyType.CLOSED
        new_company.set_company_name(company_name)
        new_company.increase_value(money)
        # Now let's create stocks for this company
        created_stocks = new_company.create_gold_stocks(stocks,client_data.uuid)
        element = CompanyStorageElement(uuid=new_company.uuid,company=new_company)
        self.__companies_storage.append(element)
        self.__amount_closed_companies += 1
        # Apply to player
        client_data.player_data.purchase_stock_confirm(new_company.uuid,company_name, created_stocks, money)
        return CompanyCreateResult.SUCCESS

    # Recalculate stock's cost of companies
    def recalculate_companies_stock_cost(self,server_time):
        for element in self.__companies_storage:
            element : CompanyStorageElement
            element['company'].recalculate_stocks_cost(server_time)

    # End function of cycle
    # Make analysis of situation and provide value changes
    def commit_company_progress(self,data: WorldSituation, server_time, game_cycle: int):
        self.game_cycle = game_cycle
        for element in self.__companies_storage:
            element : CompanyStorageElement
            cur_compnay = element['company']
            if cur_compnay.company_type is CompanyType.OPEN:
                # Open companies depend on news and nothing more
                cur_compnay.change_value_due_worldsituation(data) # change value rate
                cur_compnay.cycle_end_recalculation(game_cycle) # calculate changes of company value only based on news and world situation
                cur_compnay.recalculate_stocks_cost(server_time) # Apply new stock costs
            elif cur_compnay.company_type is CompanyType.CLOSED:
                cur_compnay.change_value_due_worldsituation(data)
                cur_compnay.decrease_rate_for_closed_company()
                cur_compnay.cycle_end_recalculation(game_cycle)
                # TODO: Here is should be method to change value due to invest situation

    # Return open companies in list for Open Exhange Market
    def get_open_companies_to_list(self):
        c_open_list = []
        # Go though all compnies to get open
        for element in self.__companies_storage:
            # To have strict typization and autocompletion. Do not blame me I'm just lazy to search
            element: CompanyStorageElement
            # If compnay is not open this method does not want it
            if element['company'].company_type != CompanyType.OPEN:
                continue
            c_open_list.append(element['company'].prepare_open_company_data())

        return c_open_list

    # Client tries to buy silver stock(s) of company
    # uuid is company uuid, amount is amount of stock, cost is a cost of one stock, client data is client data
    def purchase_stock_of_comany(self, uuid:str, amount : int, cost : float, client_data : ClientData) -> StockPurchaseResult:
        # First let's find a company
        company : Company
        company = self.company_by_uuid(uuid)
        if company == None:
            return StockPurchaseResult.NO_SUCH_COMPANY

        if amount < 1:
           return StockPurchaseResult.STOCK_AMOUNT_ERROR

        if company.silver_available_amount == 0:
            return StockPurchaseResult.NO_MORE_STOCKS

        if company.silver_available_amount < amount:
            # Can't buy requested amount of stocks. Set amount to available
            amount = company.silver_available_amount

        # Better to compare a closed value to cost. Because no problem in error in 2 digits after comma.
        close =  math.isclose(cost, company.silver_cost,rel_tol=1e-2)
        if close is not True:
            return StockPurchaseResult.STOCK_COST_ERROR

        # Calculate cost
        full_cost = amount * company.silver_cost
        if client_data.player_data.money < full_cost:
            return StockPurchaseResult.NOT_ENOUGH_MONEY

        # Buy stock for user (client), get list of stocks, which will be attached to client
        stock_list = company.purchase_silver_stock(amount,client_data.uuid)
        # Attach stocks to client, and decrease amount of money
        client_data.player_data.purchase_stock_confirm(uuid,company.name ,stock_list, full_cost)

        # Increase company value by investoring money
        company.increase_value(full_cost)
        company.recalculate_stocks_cost()
        return StockPurchaseResult.SUCCESS

    # Player tries to sell stock of open company
    def sell_stock_of_company(self, uuid: str, amount:int, client_data : ClientData) -> StockSellResult:
        # First let's find a company
        company : Company
        company = self.company_by_uuid(uuid)
        if company == None:
            return StockSellResult.NO_SUCH_COMPANY

        if amount < 1:
            return StockSellResult.NO_ENOUGH_AMOUNT

        available_amount = client_data.player_data.get_silver_amount_of_company(uuid)
        if available_amount == -1:
            # Player has not this company in his list
            return StockSellResult.HAS_NO_COMPANY
        elif available_amount < amount:
            # Player has not enough amount of stocks which he requested to sell
            return StockSellResult.NO_ENOUGH_AMOUNT

        # Calculate cost of sale
        full_cost = amount * company.silver_cost

        # Remove stocks from player and increase money
        client_data.player_data.sell_silver_stocks(uuid,amount,full_cost)
        # Decrease the compnay value, because money were taken back
        decrese_amount = -1 * full_cost
        company.increase_value(decrese_amount)
        company.recalculate_stocks_cost()
        return StockSellResult.SUCCESS

    def get_silver_stocks_history(self, c_uuid: str):
        history = []
        company : Company
        company = self.company_by_uuid(c_uuid)
        # No company return empty list
        if company == None:
            return history
        history = company.get_silver_stock_history()
        return history

    # Here will be description, that naming for companies is allowed
    def verify_syntax_new_company_name(self, name:str):
        # First check that company name has only two digits
        digits = sum(c.isdigit() for c in name)
        if digits > 2:
            return False
        return True

    # Verify, that company name is unique in existing companies
    def verify_uniq_new_company_name(self, name:str):
        for element in self.__companies_storage:
            element : CompanyStorageElement
            if element['company'].name == name:
                return False
        return True

    def verify_business_type_existance(self, b_type: int):
        try:
            c_b_t = CompanyBusinessType(b_type)
            utils.unused(c_b_t)
            return True
        except:
            return False

    # These method creates working request. Attach it to company.
    # Output is commnication related format.
    # Do not forget to sync it with communication protocol
    def create_working_plan_request(self,c_uuid: str, begin_cycle: int, end_cycle: int, target: float, w_sit: WorldSituation):
        body={
                "result":0
                }
        company = self.company_by_uuid(c_uuid)
        if company == None:
            body={
                    "result" : CompanyWorkingRequestResult.NO_SUCH_COMPANY.value
                    }
            return body
        if not company.working_verify_cycles(begin_cycle,end_cycle):
            body={
                    "result" : CompanyWorkingRequestResult.REQUEST_PERIOD_TAKEN.value
                    }
        # Create working plan
        plan = CompanyWorkingPlan(begin_cycle,end_cycle)
        inf_level = w_sit.required_influence_types_level(company.news_dependency)
        plan.request_setup(target,company.value,inf_level)
        company.working_plan_append_pending(plan)
        body={
                "result" : CompanyWorkingRequestResult.SUCCESS.value,
                "c_uuid" : company.uuid,
                "w_uuid" : plan.plan_uuid,
                "earn" : plan.earn_value,
                "lose" : plan.lose_value
                }
        return body

    def working_plan_apply(self, c_uuid: str, w_uuid: str):
        company = self.company_by_uuid(c_uuid)
        if company is None:
            return CompanyWorkingRequestResult.NO_SUCH_COMPANY
        res = company.working_plan_apply(w_uuid)
        if res:
            return CompanyWorkingRequestResult.SUCCESS
        else:
            return CompanyWorkingRequestResult.NO_SUCH_WORKING_PLAN


