from typing import TypedDict
from stock.stock import Stock, StockType

# Store stocks by it affiliance to company
class StockStorageElement():
	def __init__(self, company_uuid : str, company_name = "This is Error message"):
		self.company_uuid = company_uuid
		self.company_name = company_name
		self.stock_list : Stock = []

# Handle player data.
class PlayerData():

	@property
	def money(self):
		return self.__money

	# Support method
	def contains(list, filter):
		for x in list:
			if filter(x):
				return x
		return None

	def __init__(self):
		self.__money = 1000
		self.__stocks : StockStorageElement = []


	def get_all_silver_stocks_to_list(self) -> list:
		stocks_list = []
		if len(self.__stocks) < 1:
			return stocks_list

		for element in self.__stocks:
			element: StockStorageElement
			amount = len(element.stock_list)

			# TODO: Optimize it please!
			stocks_cost = []
			stocks_value = []
			for stock in element.stock_list:
				stocks_cost.append(stock.cost)
				stocks_value.append(stock.value)
			stock_cost_sum = sum(stocks_cost)
			stocks_value_sum = sum(stocks_value)
			# Info syntax is based on communication protocol txt
			company_info = {
				'uuid' : element.company_uuid,
				'name' : element.company_name,
				'amount': amount,
				'cost' : stock_cost_sum,
				'value': stocks_value_sum
			}
			stocks_list.append(company_info)

		return stocks_list


	# Be aware, this method should be called only after you have confirmation from comnapies handler or logic handler
	def purchase_stock_confirm(self, company_uuid : str, company_name: str, stock_list : list, cost: float):
		# decrease amount of money
		self.__money -= cost

		element = self.get_storage_element_by_uuid(company_uuid)
		if element is None:
				element = StockStorageElement(company_uuid,company_name)
				self.__stocks.append(element)
		
		for stock in stock_list:
			stock : Stock
			element.stock_list.append(stock)


	def get_storage_element_by_uuid(self, company_uuid: str):
		el = None
		for element in self.__stocks:
			element : StockStorageElement
			if element.company_uuid == company_uuid:
				el = element
				break
		return el

