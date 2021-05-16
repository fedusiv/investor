import random
import time
from uuid import uuid4
from enum import Enum

from companies.companies_types import CompanyType
from companies.companies_types import CompanyBusinessType
from companies.company_data import CompanyData
from companies.company_name_generation import CompanyNameGenerator
from stock.stock import Stock
from stock.stock import StockType


# Operate with company
class Company():

	@property
	def name(self):
		return self.data.name
	@property
	def uuid(self):
		return self.data.uuid
	@property
	def value(self):
		return self.data.value
	
	@property
	def silver_cost(self):
		for stock in self.stocks.values():
			stock : Stock
			if stock.type != StockType.SILVER:
				continue
			# itarate loop until we received first Silver stock
			return stock.cost

	@property
	def silver_full_amount(self):
		return self.__silver_amount_full
	
	@property
	def silver_available_amount(self):
		return self.__silver_amount_full - self.__silver_amount_bought


	# Init generates default random Company 
	def __init__(self):
		# Dictionary for stocks. Storage.
		# {stock_uuid : stock_object}
		self.stocks = {}

		# Create data object
		self.data = CompanyData()

		# Generate type
		random.seed(time.time())
		self.business_type : CompanyBusinessType = random.choice(list(CompanyBusinessType))
		# Generate name
		self.data.name = CompanyNameGenerator.name_generate(self.business_type)

		# Generate uniq id.
		# TODO : verify, that this is right solution
		self.data.uuid = str(uuid4())

		# Generate default random value
		random.seed(time.time())
		random_cost = random.uniform(1000.0, 5000.0)
		self.data.value = round(random_cost,2)

		# On init stage company has none type and can't participate on marketing operations
		# Assume that type will be changed further
		self.company_type = CompanyType.NONE

		self.__silver_amount_full = 0 # Amount of stocks
		self.__silver_amount_bought = 0 # Amount of stocks which are bought


	# Probably temporaty method
	# Generate 1 gold stock with 51% of value. And other of 49% with given amount
	# So full amount is 1 GOLD + amount of SILVER
	def generate_stocks51(self, amount: int):
		# Change type to open. This is kind of default stocks initialization
		self.company_type = CompanyType.OPEN
		# Create stocks
		main_stock = Stock(self.uuid, StockType.GOLD, 0.51)
		self.stocks[main_stock.uuid] = main_stock
		# Generate others
		value = (49 / amount) / 100
		for i in range(0,amount):
			stock = Stock(self.uuid, StockType.SILVER, value)
			self.stocks[stock.uuid] = stock
			self.__silver_amount_full += 1
		# After generation need to calculate stock cost
		self.recalculate_stocks_cost()

	# When company change it's value, better to recalculate stocks cost
	def recalculate_stocks_cost(self):
		for stock in self.stocks.values():
			stock.calculate_cost(self.value)

	# Companies handler calls this method.
	# Company return list of stock, that will be bought
	def purchase_silver_stock(self, amount: int, client_uuid : str) -> list:
		stock_list = []
		counter = amount
		for stock in self.stocks.values():
			stock : Stock
			if stock.type == StockType.GOLD:
				continue	# not silver go next
			if stock.bought:
				continue	# already bought go next
			counter -= 1
			stock_list.append(stock)
			stock.buy_stock(client_uuid)
			self.__silver_amount_bought += 1

			if counter <= 0:
				break

		return stock_list


	# prepare dict of open company data
	# Open company should return information about silver stocks
	def prepare_open_company_data(self):
		data = {
			'uuid' : self.uuid,
			'name' : self.name,
			'cost' : self.silver_cost
		}
		return data

	# Server debug method
	def print_company_data(self):
		print("Company name: ", self.name)
		print("\tuuid: ", self.uuid, "\tvalue: ", self.value)
		print("\tstocks:")
		print(len(self.stocks))
		for stockey in self.stocks.keys():
			print("\t",end='',flush=True)
			self.stocks[stockey].print_stock_data()

