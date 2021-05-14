# This class operates logic of clients requests and actions
# Reason is to separate operation module from client connection module

import tornado.websocket

from communication_parser import CommunitcationParserResult
from logic_handler import LogicHandler
from communication_protocol import MessageType
from communication_protocol import CommunicationProtocol
from client_data import ClientData

class ClientOperation():

	def __init__(self, ws : tornado.websocket.WebSocketHandler, logic_handler : LogicHandler):
		self.ws = ws
		self.logic_handler = logic_handler
		self.client_data : ClientData

	def parse_command(self,cmd : CommunitcationParserResult):
		switcher = {
			MessageType.COMPANIES_OPEN_LIST : self.request_open_companies_list,
			MessageType.CLIENT_DATA : self.request_client_data,
			MessageType.BUY_STOCK : self.request_to_buy_stock
		}
		func = switcher.get(cmd.result_type)
		func(cmd)

	def wrong_command(self,cmd):
		print("Wrong type")

	def request_open_companies_list(self,cmd):
		c_list = self.logic_handler.companies_open_list_client()
		c_list_msg = CommunicationProtocol.create_companies_open_list(c_list)
		self.ws.write_message(c_list_msg)

	# Send to client, client's data
	def request_client_data(self,cmd):
		s_list = self.client_data.player_data.get_all_stocks_to_list()
		client_data_msg = CommunicationProtocol.create_client_data_msg(login= self.client_data.login, money=self.client_data.player_data.money, stock_list=s_list)
		self.ws.write_message(client_data_msg)

	# Client send request to buy a stock
	def request_to_buy_stock(self,cmd : CommunitcationParserResult):
		res = self.logic_handler.request_to_buy_stock(cmd.company_uuid,cmd.stock_amount, cmd.stock_cost, self.client_data.player_data.money)
		if res is True:
			# Purchase can be done
			self.client_data.player_data.purchase_stock(cmd.company_uuid, cmd.stock_amount, cmd.stock_cost)
		s_list = self.client_data.player_data.get_all_stocks_to_list()
		result_msg = CommunicationProtocol.create_purchase_result(res, self.client_data.player_data.money, s_list)
		self.ws.write_message(result_msg)

