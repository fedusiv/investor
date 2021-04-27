from tornado.ioloop import IOLoop
from tornado import gen
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
from tornado.websocket import websocket_connect
import asyncio
from queue import Queue

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