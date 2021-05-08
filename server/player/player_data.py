
from companies.stock import Stock

# Handle player data.
class PlayerData():

	@property
	def money(self):
		return self.__money

	@property
	def amount(self):
		return self.__stocks

	# Support method
	def contains(list, filter):
		for x in list:
			if filter(x):
				return x
		return None

	def __init__(self):
		self.__money = 1000
		self.__stocks = []


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
	# This method apply purchase to player
	def purchase_stock(self, uuid: str, amout: int, cost: float):
		# Remove the price from player money amount
		self.__money -= amout * cost
		# Add to the stock storage
		cmp =  self.contains(self.__stocks, lambda x : x.uuid == uuid)
		if cmp is not None:
			# if player already has stock of this company
			cmp.amount += amout
		else:
			# If this is new company for player in stock list, need to add this
			stock = Stock(uuid,amout)
			self.__stocks.append(stock)

