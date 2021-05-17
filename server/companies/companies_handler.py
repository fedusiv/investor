from enum import Enum
import time
from typing import List, TypedDict
from communication_parser import CommunitcationParser

from companies.company import Company
from companies.companies_types import CompanyType
from player.player_data import PlayerData
from client_data import ClientData
from news.world_situation_data import WorldSituationData

MAX_COMPANIES_AMOUNT = 5

# To report result about stock purchase
class StockPurchaseResult(Enum):
	SUCCESS = 1
	NO_SUCH_COMPANY = 2
	NO_MORE_STOCKS = 3
	NOT_ENOUGH_MONEY = 4
	STOCK_COST_ERROR = 5

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

	# Get company by it's uuid
	def company_by_uuid(self, uuid: str):
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
		while len(self.__companies_storage) < MAX_COMPANIES_AMOUNT:
			# Create companies
			new_company = Company()
			# Generate default set of stocks
			new_company.generate_stocks51(15)
			element = CompanyStorageElement(uuid=new_company.uuid,company=new_company)
			self.__companies_storage.append(element)

	# Recalculate stock's cost of companies
	def recalculate_companies_stock_cost(self):
		for element in self.__companies_storage:
			element : CompanyStorageElement
			element['company'].recalculate_stocks_cost()

	# Make analysis of situation and provide value changes
	def commit_company_progress(self,data: WorldSituationData):
		for element in self.__companies_storage:
			element : CompanyStorageElement
			element['company'].change_value_due_worldsituation(data)
			element['company'].recalculate_stocks_cost()
			element['company'].print_company_values()

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
		
		if company.silver_available_amount == 0:
			return StockPurchaseResult.NO_MORE_STOCKS

		if company.silver_available_amount < amount:
			# Can't buy requested amount of stocks. Set amount to available
			amount = company.silver_available_amount
		
		if cost != company.silver_cost:
			return StockPurchaseResult.STOCK_COST_ERROR

		# Calculate cost
		full_cost = amount * company.silver_cost
		if client_data.player_data.money < full_cost:
			return StockPurchaseResult.NOT_ENOUGH_MONEY

		# Buy stock for user (client), get list of stocks, which will be attached to client
		stock_list = company.purchase_silver_stock(amount,client_data.uuid)
		# Attach stocks to client, and decrease amount of money
		client_data.player_data.purchase_stock_confirm(uuid, stock_list, full_cost)

		# Increase company value by investoring money
		company.increase_value(full_cost)

		return StockPurchaseResult.SUCCESS


