from typing import TypedDict
from stock.stock import Stock

class StockStorageElement(TypedDict):
	company_uuid : str	# company uuid
	stock : Stock

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


	def get_all_stocks_to_list(self):
		if len(self.__stocks) < 1:
			return 
		
		stocks_list = []
		for stock in self.__stocks:
			s_desc = {
				"uuid" : stock.uuid,
				"amount" : stock.amount,
			}
			stocks_list.append(s_desc)
		return stocks_list

	# Be aware, this method should be called only after you have confirmation from comnapies handler or logic handler
	def purchase_stock_confirm(self, company_uuid : str, stock_list : list, cost: float):
		# decrease amount of money
		self.__money -= cost
		for stock in stock_list:
			stock : Stock
			new_element = StockStorageElement(company_uuid=company_uuid, stock= stock)
			self.__stocks.append(new_element)
		

