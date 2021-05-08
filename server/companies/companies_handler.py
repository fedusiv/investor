from companies.company import Company
import time

MAX_COMPANIES_AMOUNT = 20

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

	#---------------------#
	#Logic part
	#---------------------#
	# dict holds all companies on a server
	# dict { "uuid" : Company(object)}
	__companies_storage = {}

	# Check current companies amount, if less create new
	def update_companies_amount(self):
		while len(self.__companies_storage) < MAX_COMPANIES_AMOUNT:
			# Create companies
			new_company = Company()
			self.__companies_storage[new_company.uuid] = new_company

	def update_companies_cost(self):
		current_time = time.time()
		# Update company cost
		for company in self.__companies_storage.values():
			if company.cost_next_update_time < current_time:
				# Need update cost
				company.generate_random_cost()
				# Set next update time
				company.generate_next_cost_update_time_random()

	def print_all_companies(self):
		for company in self.__companies_storage:
			print(company.name, company.cost)

	# Return all companies in list
	def get_all_companies_to_list(self):
		companies_desc_list = []
		for company in self.__companies_storage.values():
			c_desc = {
				"uuid" : company.uuid,
				"name" : company.name,
				"cost" : company.cost
			}
			companies_desc_list.append(c_desc)
		return companies_desc_list

	# Client tries to buy stock(s) of company
	def purchase_stock_of_comany(self, uuid:str, amount : int, cost : float, player_money : float):
		company = self.__companies_storage[uuid]
		if company is None:
			# No such kind of company
			return False
		if company.verify_in_cost_history(cost) is False:
			# Some fake or outdated cost of stock
			return False
		full_cost = amout * cost
		if player_money < full_cost:
			# Player can not afford to buy
			return False
		
		# Purchase operation of company and stock
		# TODO: in future there should be some implemenation of it

		# Player can purchase stock
		return True



