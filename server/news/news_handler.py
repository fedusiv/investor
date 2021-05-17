

import time
import random
from typing import TypedDict

from news.world_situation import WorldSituation
from news.news_element import NewsElement
import config

class NewsStorageElement(TypedDict):
	server_time : float
	event : NewsElement

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
		self.__news_storage : NewsStorageElement = []
		self.world_situation = WorldSituation()

		self.last_news_generation_time = time.time()
		self.generate_next_news_time_interval()

	
	################
	#  Logic Part  #
	################

	# Main loop for news handler
	def update_news(self, server_time: float):
		event = None
		cur_time = time.time()
		if cur_time - self.last_news_generation_time > self.next_news_generation_interval:
			#Generate news
			event = NewsElement(server_time)
			self.world_situation.change_situation(event.world_situation_data)
			self.last_news_generation_time = cur_time
			self.generate_next_news_time_interval()

			storage_element = NewsStorageElement(server_time=server_time, event=event)
			self.__news_storage.append(storage_element)
		return event

	def generate_next_news_time_interval(self):
		random.seed(time.time())
		random_interval = random.uniform(config.NEWS_GENERATION_TIME_DISPERSION[0], config.NEWS_GENERATION_TIME_DISPERSION[1])
		self.next_news_generation_interval = round(random_interval,2)

	# Prepare list of news from given time
	def get_news_list_bytime(self, time: float):
		news_list = []
		for element in self.__news_storage:
			element: NewsStorageElement
			if element["server_time"] >= time:
				# Okay we need only these news
				# Names is taken from communication protocol txt, be aware of it
				event = element["event"]
				el = {
					"theme" : event.theme,
					"source" : event.source,
					"server_time" : event.time
				}
				news_list.append(el)
		return news_list

	# Prepare last n amount of news. If amount -1 it will return all list
	def get_news_list_byamount(self, amount: int):
		news_list = []
		counter = amount
		for element in reversed(self.__news_storage):
			element: NewsStorageElement
			event = element["event"]
			el = {
				"theme" : event.theme,
				"source" : event.source,
				"server_time" : event.time
			}
			news_list.append(el)
			# If amount is -1 return list with all news
			if amount > -1:
				# If amount is determined return determined amount of values
				counter-=1
				# Until counter is not equal 0
				if counter <= 0:
					break
		news_list.reverse()	# Reverse list to keep in chronological order
		return news_list

	# Debug function for server
	def print_new_event(self, event : NewsElement):
		print("News: ",event.theme, "\tsource: ", event.source)
