import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from communication_parser import CommunitcationParser
from communication_parser import CommunitcationParserReturnCode

PORT = 3002

class Server(tornado.web.Application):

	def __init__(self):
		handlers = [(r"/", ClientHandler)]
		settings = dict(debug=True)
		tornado.web.Application.__init__(self, handlers, **settings)
		self.clients = ClientHandlers.Instance()


class ClientHandler(tornado.websocket.WebSocketHandler):

	def open(self):
		print("A client connected to server. ", self.request.remote_ip)
		# When connection happen get clientHandlers instance
		self.client_handlers = ClientHandlers.Instance()

	def on_close(self):
		print("A client disconnected")

	def on_message(self, message):
		err = CommunitcationParser.parse_clinet_message(message)
		print(err)


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
		self.__client_storage.append(client)


def ServerStart():
	server = Server()
	server.listen(PORT)
	
	# After this line nothing will act, because it starts infinite priority loop
	tornado.ioloop.IOLoop.instance().start()

