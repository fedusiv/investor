import threading
import websocket_client
from queue import Queue
import cli_parser

from tornado.ioloop import IOLoop


def create_client(queue_receive:Queue,queue_sent:Queue):
	web_client = websocket_client.WebSocClient("ws://localhost:3002/",queue_receive,queue_sent)
	thread = threading.Thread(target=websocket_client.start_client,args=(web_client,))
	thread.setDaemon(True)
	thread.start()

def cli():
	queue_receive = Queue()
	queue_sent = Queue()
	create_client(queue_receive,queue_sent)
	cli_parser.gui_run(queue_receive, queue_sent)

cli()