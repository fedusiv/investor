

import time
import random

from news.world_situation import WorldSituation
from news.news_element import NewsElement

class NewsHandler():
	# Singleton part
	__instance = None
	@staticmethod

	def Instance():
		if NewsHandler.__instance == None:
			NewsHandler()
		return NewsHandler.__instance
	
	def __init__(self):
		NewsHandler.__instance = self
		self.world_situation = WorldSituation()

		self.last_news_generation_time = time.time()
		self.generate_next_news_time_interval()

	
	################
	#  Logic Part  #
	################

	# Main loop for news handler
	def update_news(self):
		event = None
		cur_time = time.time()
		if cur_time - self.last_news_generation_time > self.next_news_generation_interval:
			#Generate news
			event = NewsElement()
			self.print_new_event(event)
			self.world_situation.change_situation(event.world_situation)
			self.last_news_generation_time = cur_time
			self.generate_next_news_time_interval()
		return event

	def generate_next_news_time_interval(self):
		random.seed(time.time())
		random_interval = random.uniform(3.0, 7.0)
		self.next_news_generation_interval = round(random_interval,2)

	# Debug function for server
	def print_new_event(self, event : NewsElement):
		print("News: ",event.theme, "\tsource: ", event.source)
