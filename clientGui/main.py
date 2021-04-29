import gui
import threading
import client
from tornado.ioloop import IOLoop
from queue import Queue

def create_client(queue_receive:Queue,queue_sent:Queue):
	cli = client.Client("ws://localhost:3002/",queue_receive,queue_sent)
	thread = threading.Thread(target=client.start_client,args=(cli,))
	thread.setDaemon(True)
	thread.start()

def main():
	queue_receive = Queue()
	queue_sent = Queue()
	create_client(queue_receive,queue_sent)
	# gui is main thread, so it need to initialized after
	ui = gui.gui_run(queue_receive, queue_sent)

if __name__ == "__main__":
	main()
