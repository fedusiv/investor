import json
import time
import random

from news.world_situation import WorldSituation
from news.world_situation_data import WorldSituationData

class NewsElement():
	def __init__(self, server_time: float):
		self.time = server_time
		with open("news/NewsList.json") as type_names:
			data = json.load(type_names)
			news_list = data["news"]
			news_amount = len(news_list)
			random.seed(time.time())
			news_id = random.randint(0,news_amount-1)	# amount-1 because list first index 0
			# Current event
			event = news_list[news_id]
			self.world_situation_data = WorldSituationData()
			# Apply points
			self.world_situation_data.military_points = event["military"]
			self.world_situation_data.food_points = event["food"]
			self.world_situation_data.scince_points = event["scince"]
			self.world_situation_data.mining_points = event["mining"]
			# Apply description
			self.theme = event["theme"]
			self.source = event["source"]
