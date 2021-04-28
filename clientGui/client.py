from tornado.ioloop import IOLoop
from tornado import gen
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
from tornado.websocket import websocket_connect
import asyncio
from queue import Queue
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from server.communication_protocol import CommunicationProtocol

# Logic part of connection based on qt for gui object.
class ClientQObject(QObject):
	def __init__(self,queue: Queue):
		super().__init__()
		self.queue = queue
		self.queue_timer = QTimer(self)
		self.queue_timer.timeout.connect(self.queueChecker)
		# zaebalsya to play with asyncio, better to use gui/qt for timer functionality to operate with qt inside qt
		self.queue_timer.setInterval(10)	# each 10ms call func to check queue messages from websocket
		self.queue_timer.start()

	def queueChecker(self):
		if self.queue.qsize() > 0:
			# get message from websocket and parse it
			msg = self.queue.get()

	def transfer_login_auth(self, login, password):
		# prepare message
		msg = CommunicationProtocol.create_login_msg(login,password)
		# sent message to websocket queue
		
	


class Client():
	def __init__(self, url,queue : Queue):
		self.url = url
		self.ws = None
		self.queue = queue
	
	def start(self):
		print("start")
		
		self.connect()
		self.io_loop = IOLoop.current()
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
		self.queue.put(message)


def start_client(client):
	# important method allows to use asyncio with any thread we want. Basically we need just one for websocket
	asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
	client.start()