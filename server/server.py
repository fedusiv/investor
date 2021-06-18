import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time

import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options
from tornado import gen

from client.client_handler import ClientHandler, ClientsHandler
from logic_handler import LogicHandler
from users_dao import UsersDao
import config


class Server(tornado.web.Application):

    def __init__(self, io_loop):
        handlers = [(r"/", ClientHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)
        self.clients = ClientsHandler.Instance()
        self.io_loop = io_loop
        # Rise invinite loop for keep alive checker
        self.io_loop.spawn_callback(self.keep_alive_loop)

        # Init data base
        self.users_dao = UsersDao.Instance()

        # Logic part
        self.logic_handler = LogicHandler.Instance()
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


def ServerStart():
    io_loop_instance = tornado.ioloop.IOLoop.current()
    server = Server(io_loop_instance)
    server.listen(config.PORT)

    # After this line nothing will act, because it starts infinite priority loop
    print("Server is starting")
    io_loop_instance.start()


