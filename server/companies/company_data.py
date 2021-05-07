# Store data of company
class CompanyData():
	name = ""
	uuid = ""
	cost = 0.0
	def __init__(self, name = "", uuid = "", cost = 0.0):
		self.name = name
		self.uuid = uuid
		self.cost = cost
