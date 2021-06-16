from uuid import uuid4

# Working plan is company value change mechanism
# Owner sets how company can be extended and make some prognosis
# Working plan is a information about it for a company
class CompanyWorkingPlan():
    def __init__(self, begin_cycle: int, end_cycle: int):
        self.start_cycle = begin_cycle
        self.end_cycle = end_cycle
        # Need to track working plans
        self.plan_uuid = str(uuid4())
        # Applied, means, that company is working on that plan now
        self.applied = False

    def request_setup(self, request_target: float, company_value : float, inf_level: int):
        self.end_value = request_target

        # If there is a good situation level of earn should be less and vise versa
        inf_value = 1 - (0.05 * inf_level)
        period = self.end_cycle - self.start_cycle + 1
        diff = request_target / company_value
        # The more period of waiting then less additional earn and more lose
        # The less period of waiting then more earn and less lose
        if diff < 1:
            earn_koef = pow(diff,period)
            lose_koef = pow(diff,1/period)
        else:
            earn_koef = pow(diff,1/period)
            lose_koef = diff * pow(period, 1/2)
        # Earn calculates based on request target
        self.earn_value = request_target * earn_koef * inf_value
        # Lose value calculates based on company current value
        self.lose_value = company_value * lose_koef * inf_value
