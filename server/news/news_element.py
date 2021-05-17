import json
import time
import random

from news.world_situation import WorldSituation

class NewsElement():
	def __init__(self):
		with open("news/NewsList.json") as type_names:
			data = json.load(type_names)
			news_list = data["news"]
			news_amount = len(news_list)
			random.seed(time.time())
			news_id = random.randint(0,news_amount-1)	# amount-1 because list first index 0
			# Current event
			event = news_list[news_id]
			self.world_situation = WorldSituation()
			# Apply points
			self.world_situation.military_points = event["military"]
			self.world_situation.food_points = event["food"]
			self.world_situation.scince_points = event["scince"]
			self.world_situation.mining_points = event["mining"]
			# Apply description
			self.theme = event["theme"]
			self.source = event["source"]
