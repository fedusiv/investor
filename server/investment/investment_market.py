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
                                        invest_value: float,
                                        i_type: int,
                                        payback_value: float,
                                        cycle_period: int):
        # Create investment plan
        plan = InvestmentPlan(c_uuid,InvestmentType(i_type),invest_value,payback_value,cycle_period)
        element = InvestmentMarketStorageElement(server_time=server_time,plan=plan)
        # Place it in a storage
        self._market_storage.append(element)


