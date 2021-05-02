import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options
from tornado import gen
from tornado.options import define, options
from communication_parser import CommunitcationParser
from communication_parser import CommunitcationParserResult
from communication_protocol import MessageType
from communication_protocol import CommunicationProtocol
import time
from logic_handler import LogicHandler

PORT = 3002
KEEP_ALIVE_TIME = 2
KEEP_ALIVE_ERROR = 5

class Server(tornado.web.Application):

	def __init__(self, io_loop):
		handlers = [(r"/", ClientHandler)]
		settings = dict(debug=True)
		tornado.web.Application.__init__(self, handlers, **settings)
		self.clients = ClientHandlers.Instance()
		self.io_loop = io_loop
		# Rise invinite loop for keep alive checker
		self.io_loop.spawn_callback(self.keep_alive_loop)

                # Logic part
		self.logic_handler = LogicHandler()
		self.io_loop.spawn_callback(self.logic_handler.logic_loop)


	# go through all clients to check if need to send keep alive
	# each defined time in gen.sleep, it goes through all clients required to keep alive
	async def keep_alive_loop(self):
		while True:
			silent_clients = self.clients.list_probably_dead_clients()
			if silent_clients != None:
				for client in silent_clients:
					client.send_keep_alive()
					client.alive_last_msg_time = time.time()
			await gen.sleep(0.1)


class ClientHandler(tornado.websocket.WebSocketHandler):

	# Store value, when client was alive last time, if it less than KEEP_ALIVE_TIME, need to send message and check if it is still communicative
	alive_time = 0.0
	# Error count, if it reaches KEEP_ALIVE_ERROR so client is dead and can be disconneceted
	alive_error = 0
	# Store value, when keep_alive message was sent last time
	alive_last_msg_time = 0.0
	

	def open(self):
		print("A client connected to server. ", self.request.remote_ip)
		# When connection happen get clientHandlers instance
		self.client_handlers = ClientHandlers.Instance()

	# Required this field for web gui
	def check_origin(self, origin):
		return True
	
	def on_close(self):
		print("A client disconnected")
		self.client_handlers.remove_connected_client(self)

	def on_message(self, message):
		# Got message, client alive. Store time for that
		self.alive_time  = time.time()
		self.alive_error = 0
		result : CommunitcationParserResult = CommunitcationParser.parse_clinet_message(message)
		if result.err is False:
			# end execution, wrong message
			return
		# messages related to connection should be proceed here, other need to be sent to separate command executtion module
		if result.result_type == MessageType.KEEP_ALIVE:
			# do nothing. This is just keep alive. Server now knows, that client is alive
			return
		elif result.result_type == MessageType.LOGIN:
			self.on_logged()
		else:
			self.command_execution()

	def on_logged(self):
		self.client_handlers.store_connected_client(self)
		print("client logged in")
		# send message to client
		msg = CommunicationProtocol.create_login_result_msg(True)
		self.write_message(msg)

	def send_keep_alive(self):
		msg = CommunicationProtocol.create_keep_alive_msg()
		self.write_message(msg)

	def command_execution(self):
		print("command execution")

# Singleton to store all handlers
# And manipulate them
class ClientHandlers():
	# Singleton part
	__instance = None
	@staticmethod

	def Instance():
		if ClientHandlers.__instance == None:
			ClientHandlers()
		return ClientHandlers.__instance
	
	def __init__(self):
		ClientHandlers.__instance = self

	# Functionality part
	__client_storage = []
	def store_connected_client(self, client: ClientHandler):
		if client in self.__client_storage:
			# do nothing it's already there
			return
		self.__client_storage.append(client)
	
	def remove_connected_client(self, client: ClientHandler):
		self.__client_storage.remove(client)

	# Return the list of clients, that KEEP_ALIVE_TIME did not send any message
	# If error is bigger disconnect
	def list_probably_dead_clients(self):
		silent_clients = []
		for client in self.__client_storage:
			if client.alive_error > KEEP_ALIVE_ERROR:
				client.close()
				# disconnect
				continue
			if client.alive_error > 0:
				if time.time() - client.alive_last_msg_time > KEEP_ALIVE_TIME:
					# need to send message of keep_alive. Did not received after previous time
					client.alive_error +=1
					silent_clients.append(client)
				continue
			if client.alive_error == 0:
				# check if client keep alive time is not less than KEEP_ALIVE_TIME
				if time.time() - client.alive_time > KEEP_ALIVE_TIME:
					client.alive_error +=1
					silent_clients.append(client)
		return silent_clients

def ServerStart():
	io_loop_instance = tornado.ioloop.IOLoop.current()
	server = Server(io_loop_instance)
	server.listen(PORT)
	
	# After this line nothing will act, because it starts infinite priority loop
	io_loop_instance.start()


