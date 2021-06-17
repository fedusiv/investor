from uuid import uuid4

from investment.investment_types import InvestmentType

class InvestmentPlan():
    def __init__(self, c_uuid: str, c_name: str, i_type: InvestmentType, i_value: float, p_value: float, cycle_period: int):
        self.invest_uuid = str(uuid4())
        # Investment plan is a contract between player and company
        self.company_uuid = c_uuid
        self.company_name = c_name
        # Once investment plan has player_uuid means, invesment plan applied and it's working
        self.player_uuid = ""
        self.invest_type = i_type
        # What amount of money company should receive
        self.investment_value = i_value
        # Value represent what amount of money investment plan should return to player
        # Depends on type it represent different meanings
        self.payback_value = p_value
        # Cycles period, after what amount of cycles investment should be payback.
        # If zero payback on request
        self.cycle_period = cycle_period
        # Amount of money company get since investment plan has started to work
        self.earn_value = 0.0
        # On what cycle invest plan should be destroyed and pay everything.
        # If zero invest plan will be destroyed on request
        self.end_cycle = 0
        # Flag represent, that investment process has started and investment plan can not be changed
        self.in_process = False

    # Put investment plan to a production!
    def set_to_production(self, player_uuid, cur_cycle: int):
        self.player_uuid = player_uuid
        # cycle period of investment plan, end cycle should be also 0. Because this investment works until requires
        if self.cycle_period != 0:
            self.end_cycle = cur_cycle + self.cycle_period
