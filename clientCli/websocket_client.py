from tornado.ioloop import IOLoop
from tornado import gen
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
from tornado.websocket import websocket_connect
from tornado.websocket import WebSocketClientConnection
import asyncio
from queue import Queue

# Websocket client
class WebSocClient():
	def __init__(self, url,queue_read: Queue,queue_sent: Queue):
		self.url = url
		self.ws : WebSocketClientConnection
		self.queue_read = queue_read
		self.queue_sent = queue_sent
	
	def start(self):
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

	# async loop, which triggers in 50 ms
	async def on_sent_loop(self):
		while True:
			await self.sent_message()
			# sleep 100 msec and check if it is possible to send message again
			await gen.sleep(0.05)

def start_client(client):
	# important method allows to use asyncio with any thread we want. Basically we need just one for websocket
	asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
	client.start()
