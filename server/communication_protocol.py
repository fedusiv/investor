import json
from enum import Enum

class MessageType(Enum):
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

	@staticmethod
	def create_login_msg(login,password):
		body = [login,password]
		msg = {"type" : MessageType.LOGIN.value,
				"body" : body}
		print(msg)
		msg_json = json.dumps(msg)
		return msg_json

