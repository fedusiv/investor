import gui
import threading
import client
from tornado.ioloop import IOLoop
from queue import Queue

def create_client(queue:Queue):
	cli = client.Client("ws://localhost:3002/",queue)
	thread = threading.Thread(target=client.start_client,args=(cli,))
	thread.setDaemon(True)
	thread.start()

def main():
	thread_queue = Queue()
	create_client(thread_queue)
	# gui is main thread, so it need to initialized after
	ui = gui.gui_run(thread_queue)

if __name__ == "__main__":
	main()
