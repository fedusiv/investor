from news.world_situation_data import WorldSituationData

class WorldSituation():

	def __init__(self):
		self.data = WorldSituationData()

	def change_situation(self, changes:WorldSituationData):
		self.data.military_points += changes.military_points
		self.data.food_points += changes.food_points
		self.data.scince_points += changes.scince_points
		self.data.mining_points += changes.mining_points
