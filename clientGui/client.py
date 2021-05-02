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
from server.communication_protocol import CommunicationProtocol
from server.communication_protocol import MessageType


# Logic part of connection based on qt for gui object.
class ClientQObject(QObject):
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

	def queueChecker(self):
		if self.queue_read.qsize() > 0:
			# get message from websocket and parse it
			msg = self.queue_read.get()
			self.parse_server_message(msg)
	
	def none_message_reaction(self):
		print(self.none_message_reaction.__name__)

	def parse_server_message(self,msg):
		# message should be json
		msg = CommunicationProtocol.verify_msg(msg)
		if msg is None:
			return

		# In current realization parsing and execution proccess realized in client module. If you want please spearate it
		# TODO: separate parsing to different module, not in client
		switcher = {
			MessageType.LOGIN.value : self.on_login_request_answer,
			MessageType.KEEP_ALIVE.value : self.on_keep_alive_request
		}
		func = switcher.get(int(msg["type"]), self.none_message_reaction)
		func(msg)

	def on_keep_alive_request(self,msg):
		# server wants keep alive. Just send him to inform, that client is alive
		msg_json = CommunicationProtocol.create_keep_alive_msg()
		# put to sent queue
		self.queue_sent.put(msg_json)

	def on_login_request_answer(self,msg):
		body = msg["body"]
		if body["result"] is True:
			# successfully logged
			print("logged")
		else:
			# error in login
			return

	def transfer_login_auth(self, login, password):
		# prepare message
		msg = CommunicationProtocol.create_login_msg(login,password)
		# sent message to websocket queue
		self.queue_sent.put(msg)

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
