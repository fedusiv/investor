import json
from enum import Enum

class MessageType(Enum):
	NONE = 0
	LOGIN = 1
	REGISTRATION = 2
	KEEP_ALIVE = 3
	COMPANIES_LIST_ALL = 4
	BUY_STOCK = 5
	CLIENT_DATA = 6


# Class to parse and create required messages
# This class used for server and client as well
class CommunicationProtocol():

	# Convert received message from json to required type and return in
	# if error return None
	@staticmethod
	def verify_msg(msg):
		# TODO there should be normal verification and deserialization. Also can be used custom class for deserialization
		message = json.loads(msg)
		return message

	@staticmethod
	def formulate_message(body,msg_type):
		msg = {"type" : msg_type,
			"body" : body}
		msg_json = json.dumps(msg)
		return msg_json

	# To client.
	@staticmethod
	def create_login_result_msg(result,uuid:str, msg = ""):
		body = {
			"result" : result,
			"message" : msg,
			"uuid" : uuid
		}
		msg_json = CommunicationProtocol.formulate_message(body, MessageType.LOGIN.value)
		return msg_json

	@staticmethod
	def create_keep_alive_msg():
		body = {}
		msg_json = CommunicationProtocol.formulate_message(body, MessageType.KEEP_ALIVE.value)
		return msg_json

	# To client send list with all companies
	@staticmethod 
	def create_companies_all_list(c_list):
		body = {
			"amount" : len(c_list),
			"list" : c_list
		}
		msg_json = CommunicationProtocol.formulate_message(body, MessageType.COMPANIES_LIST_ALL.value)
		return msg_json

	# To client, send client's data
	@staticmethod
	def create_client_data_msg(login : str, money : float, stock_list):
		s_list = {}
		if stock_list is not None:
			s_list = stock_list
		
		body = {
			"login" : login,
			"player_data":
			{
				"money" : money,
				"stocks" :
				{
					"amount" : len(s_list),
					"list" : s_list
				}
			}
		}
		msg_json = CommunicationProtocol.formulate_message(body, MessageType.CLIENT_DATA.value)
		return msg_json

	# To client, send result of perchase
	@staticmethod
	def create_purchase_result(result : bool, money : float, stock_list):
		body = {
			"result" : result,
			"message" : "...emppty...",	# This is temporary solution. In future it should be change to real message
			"player_data":
			{
				"money" : money,
				"stocks" :
				{
					"amount" : len(stock_list),
					"list" : stock_list
				}
			}
		}
		msg_json = CommunicationProtocol.formulate_message(body, MessageType.BUY_STOCK.value)
		return msg_json
