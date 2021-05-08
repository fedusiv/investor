from tornado import gen
from companies.companies_handler import CompaniesHandler
import time

# logic loop will work 50 times in second
LOOP_UPDATE_TIME = 0.02

class LogicHandler():
	# Singleton part
	__instance = None
	@staticmethod

	def Instance():
		if LogicHandler.__instance == None:
			LogicHandler()
		return LogicHandler.__instance
	
	def __init__(self):
		LogicHandler.__instance = self
		self.companies_handler = CompaniesHandler.Instance()

	#---------------------#
	#Logic part
	#---------------------#

	async def logic_loop(self):
		while True:
			self.companies_handler.update_companies_amount()
			self.companies_handler.update_companies_cost()
			await gen.sleep(LOOP_UPDATE_TIME)


	# Client request information about companies. Server return it
	def companies_all_list_client(self):
		return self.companies_handler.get_all_companies_to_list()

	# Client request to buy stock
	def request_to_buy_stock(self,uuid:str, amount : int, cost : float, player_money : float):
		return self.companies_handler.purchase_stock_of_comany(uuid,amount,cost,player_money)
