import json

from server.communication_protocol import MessageType

# Unlike server communication protocal, this object is not static.
class CliProtocol():

	def __init__(self):
		self.uuid = ""

	# Convert received message from json to required type and return in
	# if error return None
	def verify_msg(self, msg):
		# TODO there should be normal verification and deserialization. Also can be used custom class for deserialization
		message = json.loads(msg)
		return message

	def formulate_message(self,body,msg_type):
		msg = {"type" : msg_type,
			"body" : body,
			"uuid" : self.uuid}
		msg_json = json.dumps(msg)
		return msg_json

	# To server
	def create_login_msg(self,login,password):
		body = {"login" : login,
				"password" : password,
				"admin" : True}
		msg_json = self.formulate_message(body, MessageType.LOGIN.value)
		return msg_json

	# To server. Client requets list of all companies avalibale
	def request_open_companies_list(self):
		body = {}
		msg_json = self.formulate_message(body, MessageType.COMPANIES_OPEN_LIST.value)
		return msg_json

	# Keep alive. It's and in the Afrika keep alive
	def create_keep_alive_msg(self):
		body = {}
		msg_json = self.formulate_message(body, MessageType.KEEP_ALIVE.value)
		return msg_json

	# Send request for recieving client data
	def request_client_data(self):
		body = {}
		msg_json = self.formulate_message(body, MessageType.CLIENT_DATA.value)
		return msg_json

	def request_stock_purchase(self, company_uuid: str, amount: int, cost: float):
		body = {
			'uuid' : company_uuid,
			'amount' : amount,
			'cost' : cost
		}
		msg_json = self.formulate_message(body, MessageType.BUY_STOCK.value)
		return msg_json

	def request_stock_sell(self, company_uuid: str, amount: int):
		body = {
			'uuid' : company_uuid,
			'amount' : amount
		}
		msg_json = self.formulate_message(body, MessageType.SELL_SILVER_STOCK.value)
		return msg_json
	

	def request_news_bytime(self, time):
		body = {
			'time' : time
		}
		msg_json = self.formulate_message(body, MessageType.NEWS_BY_TIME.value)
		return msg_json

	def request_news_byamount(self, amount):
		body = {
			'amount' : amount
		}
		msg_json = self.formulate_message(body, MessageType.NEWS_BY_AMOUNT.value)
		return msg_json

	def send_global_message(self, text):
		body = {
			'type' : 1,
			'text' : text
		}
		msg_json = self.formulate_message(body, MessageType.MESSAGING.value)
		return msg_json
