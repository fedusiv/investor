from tornado.ioloop import IOLoop
from tornado import gen
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
from tornado.websocket import websocket_connect
from tornado.websocket import WebSocketClientConnection
import asyncio
from queue import Queue
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client_protocol import ClientProtocol
from server.communication_protocol import MessageType

from command_parser import CommandParser


# Logic part of connection based on qt for gui object.
class ClientQObject(QObject):

	# Flag of login state
	is_logged = False

	def __init__(self,queue_read: Queue,queue_sent: Queue):
		super().__init__()
		self.queue_read = queue_read
		self.queue_sent = queue_sent
		
		# queue_read Timer initialization
		self.queue_timer = QTimer(self)
		self.queue_timer.timeout.connect(self.queueChecker)
		# Better to use gui/qt for timer functionality to operate with qt inside qt
		self.queue_timer.setInterval(10)	# each 10ms call func to check queue messages from websocket
		self.queue_timer.start()

		# Init command parse
		self.cmd_parser = CommandParser()
		# Create communication protocol
		self.protocol = ClientProtocol()


	# Signals
	login_received = pyqtSignal(bool)	# when received login result
	companies_list_received = pyqtSignal(list)	# received list of companies
	cliend_data_received = pyqtSignal(dict)	# recived data with client information

	# Check reading queue
	def queueChecker(self):
		if self.queue_read.qsize() > 0:
			# get message from websocket and parse it
			msg = self.queue_read.get()
			self.parse_server_message(msg)

	# Parse everything, that is not related to communication
	def not_connection_messages(self, msg):
		if self.is_logged is False:
			return
		res = self.cmd_parser.parse(msg)
		return res

	def parse_server_message(self,msg):
		# message should be json
		msg = self.protocol.verify_msg(msg)
		if msg is None:
			return

		switcher = {
			MessageType.LOGIN.value : self.on_login_request_answer,
			MessageType.KEEP_ALIVE.value : self.on_keep_alive_request
		}
		func = switcher.get(int(msg["type"]), self.not_connection_messages)
		res = func(msg)
		# After parsing need to make some stuff with received and parsed information
		# TODO : make it more clearly and optimized
		if res is not None:
			if int(msg["type"]) == MessageType.COMPANIES_LIST_ALL.value:
				self.companies_list_received.emit(res)
			elif int(msg["type"]) == MessageType.CLIENT_DATA.value:
				self.cliend_data_received.emit(res)
			


	def on_keep_alive_request(self,msg):
		# server wants keep alive. Just send him to inform, that client is alive
		msg_json = self.protocol.create_keep_alive_msg()
		# put to sent queue
		self.queue_sent.put(msg_json)

	def on_login_request_answer(self,msg):
		if self.is_logged:
			# This functionality can be used only player is not logged into system
			return
		body = msg["body"]
		self.is_logged = body["result"]
		self.protocol.uuid = body["uuid"]	# Store uuid. Client will use it in communication with server for better indentification
		self.login_received.emit(self.is_logged)


	def transfer_login_auth(self, login, password):
		# prepare message
		msg = self.protocol.create_login_msg(login,password)
		# sent message to websocket queue
		self.queue_sent.put(msg)

	def send_companies_list_request(self):
		msg_json = self.protocol.request_companies_list()
		self.queue_sent.put(msg_json)

	def send_client_data_request(self):
		msg_json = self.protocol.request_client_data()
		self.queue_sent.put(msg_json)


# Connection part of client
class Client():
	def __init__(self, url,queue_read: Queue,queue_sent: Queue):
		self.url = url
		self.ws : WebSocketClientConnection
		self.queue_read = queue_read
		self.queue_sent = queue_sent
	
	def start(self):
		print("start")
		
		self.connect()
		self.io_loop = IOLoop.current()
		self.io_loop.spawn_callback(self.on_sent_loop)	# enable loop to check if there is any message awaits to be sent
		# After this start loop and nothing will work
		self.io_loop.start()
	
	@gen.coroutine
	def connect(self):
		print ("trying to connect")
		try:
			self.ws = yield websocket_connect(self.url, on_message_callback=self.on_message)
		except Exception as e:
			print ("connection error: ",e)
		else:
			print ("connected")
	
	def on_message(self,message):
		if message is None:
			# server disconnected client
			# TODO make reconnect mechanism, self.ws does not exist anymore
			self.connect()
			return
		else:
			self.queue_read.put(message)

	async def sent_message(self):
		if self.queue_sent.qsize() > 0:
			msg = self.queue_sent.get()
			self.ws.write_message(msg)

	# async loop, which triggers in 100 ms
	async def on_sent_loop(self):
		while True:
			await self.sent_message()
			# sleep 100 msec and check if it is possible to send message again
			await gen.sleep(0.1)


def start_client(client):
	# important method allows to use asyncio with any thread we want. Basically we need just one for websocket
	asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
	client.start()
