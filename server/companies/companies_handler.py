import time
from typing import List, TypedDict

from companies.company import Company, CompanyType

MAX_COMPANIES_AMOUNT = 5

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
		# 	for easier operations with it
		self.__companies_storage : CompanyStorageElement = []

	#---------------------#
	#Logic part
	#---------------------#


	# Main loop of companies handler. It is called from logic handler
	def update_companies(self):
		self.update_companies_amount()
		self.get_open_companies_to_list()

	# Check current companies amount, if less create new
	def update_companies_amount(self):
		while len(self.__companies_storage) < MAX_COMPANIES_AMOUNT:
			# Create companies
			new_company = Company()
			# Generate default set of stocks
			new_company.generate_stocks51(15)
			element : CompanyStorageElement = {'uuid' : new_company.uuid, 'company' : new_company}
			self.__companies_storage.append(element)

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

	# Client tries to buy stock(s) of company
	def purchase_stock_of_comany(self, uuid:str, amount : int, cost : float, player_money : float):
		pass



