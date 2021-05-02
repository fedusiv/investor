import json
from enum import Enum

class MessageType(Enum):
	NONE = 0
	LOGIN = 1
	REGISTRATION = 2
	KEEP_ALIVE = 3
	COMPANIES_LIST_ALL = 4


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

	# To server
	@staticmethod
	def create_login_msg(login,password):
		body = {"login" : login,
				"password" : password}
		msg_json = CommunicationProtocol.formulate_message(body, MessageType.LOGIN.value)
		return msg_json

	# To client
	@staticmethod
	def create_login_result_msg(result, msg = ""):
		body = {
			"result" : result,
			"message" : msg
		}
		msg_json = CommunicationProtocol.formulate_message(body, MessageType.LOGIN.value)
		return msg_json

	@staticmethod
	def create_keep_alive_msg():
		body = {}
		msg_json = CommunicationProtocol.formulate_message(body, MessageType.KEEP_ALIVE.value)
		return msg_json

	# To server. Client requets list of all companies avalibale
	@staticmethod
	def request_companies_list():
		body = {}
		msg_json = CommunicationProtocol.formulate_message(body, MessageType.COMPANIES_LIST_ALL.value)
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

