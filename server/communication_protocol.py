import json
from enum import Enum

class MessageType(Enum):
	NONE = 0
	LOGIN = 1
	REGISTRATION = 2


# Class to parse and create required messages
class CommunicationProtocol():

	# Convert received message from json to required type and return in
	# if error return None
	@staticmethod
	def verify_msg(msg):
		# TODO there should be normal verification and deserialization. Also can be used custom class for deserialization
		message = json.loads(msg)
		return message

	# To server
	@staticmethod
	def create_login_msg(login,password):
		body = [login,password]
		msg = {"type" : MessageType.LOGIN.value,
				"body" : body}
		msg_json = json.dumps(msg)
		return msg_json

	# To client
	@staticmethod
	def create_login_result_msg(result, msg = ""):
		body = {
			"result" : result,
			"message" : msg
		}
		msg = {"type" : MessageType.LOGIN.value,
				"body" : body}
		msg_json = json.dumps(msg)
		return msg_json


