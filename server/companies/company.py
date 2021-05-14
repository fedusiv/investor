import random
import time
from uuid import uuid4
from enum import Enum

from companies.company_data import CompanyData
from stock.stock import Stock
from stock.stock import StockType


company_type=("Forge","Quarry","Sawmill", "Mill", "Farm", "Alchemistry", "Pharmacy", "Jewellery")
owner_name=('Leidron Endas','Shrierpuld Fihlusols','Zhanreir Talmirnord', 'Krelul Keva', 'Linbak Denma', "Samneld Grunholz", "Kircard Bamberg", "Dudrik Steinlich")

# This type represent in what stage company is now
# None means, company is not initialized properly or it has no stocks
# Open means, that everyone can buy stocks
# Closed means, that company is kind on investing process, and only few users can buy it
class CompanyType(Enum):
	NONE = 0
	OPEN = 1
	CLOSED = 2

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


	# Init generates default random Company 
	def __init__(self):
		# Dictionary for stocks. Storage.
		# {stock_uuid : stock_object}
		self.stocks = {}

		# Create data object
		self.data = CompanyData()

		# Generate name
		random.seed(time.time())
		self.data.name = random.choice(company_type) + " of " + random.choice(owner_name)

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
		# After generation need to calculate stock cost
		self.recalculate_stocks_cost()

	# When company change it's value, better to recalculate stocks cost
	def recalculate_stocks_cost(self):
		for stock in self.stocks.values():
			stock.calculate_cost(self.value)

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

