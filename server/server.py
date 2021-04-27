#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options

from tornado.options import define, options

PORT = 3002

class Server(tornado.web.Application):

	def __init__(self):
		handlers = [(r"/", ClientHandler)]
		settings = dict(debug=True)
		tornado.web.Application.__init__(self, handlers, **settings)

class ClientHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print("A client connected.")
		self.write_message("CONN")

	def on_close(self):
		print("A client disconnected")

	def on_message(self, message):
		print("message: {}".format(message))



def ServerStart():
	server = Server()
	server.listen(PORT)
	tornado.ioloop.IOLoop.instance().start()

