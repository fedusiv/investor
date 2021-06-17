from typing import TypedDict

from investment.investment_plan import InvestmentPlan
from investment.investment_types import InvestmentType

class InvestmentMarketStorageElement(TypedDict):
    server_time : float
    plan : InvestmentPlan

class InvestmentMarket():
    # Singleton part
    __instance = None
    @staticmethod

    def Instance():
        if InvestmentMarket.__instance == None:
            InvestmentMarket()
        return InvestmentMarket.__instance

    def __init__(self):
        InvestmentMarket.__instance = self
        self._market_storage = []

    ##############
    # Logic Part #
    ##############

    def create_and_post_investment_plan(self, server_time: float,
                                        c_uuid: str,
                                        c_name: str,
                                        invest_value: float,
                                        i_type: int,
                                        payback_value: float,
                                        cycle_period: int):
        # Create investment plan
        plan = InvestmentPlan(c_uuid,c_name,InvestmentType(i_type),invest_value,payback_value,cycle_period)
        element = InvestmentMarketStorageElement(server_time=server_time,plan=plan)
        # Place it in a storage
        self._market_storage.append(element)
        # Return plan to attach to a company
        return plan

    # List of invesment market elements.
    # This method is related to communication protocol description. Please do not forget to sync with it
    def list_of_investment_offers(self):
        elements_list = []
        for element in self._market_storage:
            element : InvestmentMarketStorageElement
            el = {
                    "server_time" : element['server_time'],
                    "i_uuid" : element['plan'].invest_uuid,
                    "c_uuid" : element['plan'].company_uuid,
                    "c_name" : element['plan'].company_name,
                    "i_value" : element['plan'].investment_value,
                    "type" : element['plan'].invest_type.value,
                    "p_value" : element['plan'].payback_value,
                    "cycle" : element['plan'].cycle_period
                    }
            elements_list.append(el)
        body = {
                "amount" : len(elements_list),
                "list" : elements_list
                }
        return body

    # Player request to make investment
    # Verify that insetment plan exists and return it further
    def make_investment(self, i_uuid: str):
        plan = None
        for element in self._market_storage:
            element : InvestmentMarketStorageElement
            if element["plan"].invest_uuid == i_uuid:
                plan = element["plan"]
                # Set plan in process. No one can edit now.
                plan.in_process = True
                # Remove, this is no more in a market
                self._market_storage.remove(plan)
                return plan
        return plan

