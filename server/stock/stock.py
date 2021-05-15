import enum
import uuid


from enum import Enum

class StockType(Enum):
	SILVER = 1	# Silver level is common level of stock. It has cost: (value - all gold stocks)/ amount_of_silver
	GOLD = 2	# Gold has it's own "custom" value. They usually can not be obtain from opensource

# Stock entity
# I suggest do not use here public variables. To be ensure, that it will somewhere by mistake changed
class Stock():

	@property
	def uuid(self):
		return self.__uuid

	@property
	def company_uuid(self):
		return self.__c_uuid

	# Value stored in real value. So if it is 12%, value should be 0.12
	@property
	def value(self):
		return self.__value

	@property
	def type(self):
		return self.__type

	@property
	def cost(self):
		return self.__cost

	@property
	def bought(self):
		return self.__bought

	@property
	def client_uuid(self):
		return self.__client_uuid

	# When inits it should return uuid of stock
	# c_uuid - company id, wwhich stock belongs to
	# type - type of stock
	# value - what stock is a part of company value
	def __init__(self, c_uuid : str, type : StockType, value : float):
		self.__c_uuid = c_uuid
		self.__type = type
		self.__value = value

		# Generate unique id
		# TODO : check if it's good usage of uuid
		self.__uuid = str(uuid.uuid4())
		# Storage of last cost of it. Need to compensate connection delay.
		# Player can request to buy on one prices, but since this time real price can be changed. And do not to fine player, just keep last prices. But only for some amount time.
		# TODO: make it dependence of time
		self.cost_storage = []

		# Flag means, that stock is available to buy
		self.__bought = False
		# When player bought it, also better to store id of owner
		self.__client_uuid = ""

	# Calculate stock cost based on company value
	def calculate_cost(self, company_value : float):
		self.__cost = company_value * self.value
		self.cost_storage.append(self.__cost)

	# Set stock into bought state
	def buy_stock(self, client_uuid : str):
		self.__bought = True
		self.__client_uuid = client_uuid

	# Verify, that cost is valid
	def is_valid_cost(self, cost: float) -> bool:
		res = False
		if cost in self.cost_storage:
			res = True
		return res

	# For debug
	def print_stock_data(self):
		print("uuid: ", self.uuid, "\tcompany uuid: ", self.company_uuid, "\tvalue: ", self.value, "\ttype", self.type, "\tcost: ", self.cost)


