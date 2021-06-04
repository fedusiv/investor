# Store data of company
class CompanyData():

    def __init__(self, name = "", uuid = "", value = 1000.0):
        self.name = name
        self.uuid = uuid
        self.value = value
        # Stores the value of company at the beginning of cycle
        self.cycle_start_value = value
