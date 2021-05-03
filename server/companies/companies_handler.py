from companies.company import Company
import time

MAX_COMPANIES_AMOUNT = 10

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
	# list holds all companies on a server
	__companies_storage = []

	# Check current companies amount, if less create new
	def update_companies_amount(self):
		while len(self.__companies_storage) < MAX_COMPANIES_AMOUNT:
			# Create companies
			new_comapany = Company()
			self.__companies_storage.append(new_comapany)

	def update_companies_cost(self):
		current_time = time.time()
		# Update company cost
		for company in self.__companies_storage:
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
		for company in self.__companies_storage:
			c_desc = {
				"uuid" : company.uuid,
				"name" : company.name,
				"cost" : company.cost
			}
			companies_desc_list.append(c_desc)
		return companies_desc_list




