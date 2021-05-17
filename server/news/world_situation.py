# Describes world's situation. Each parameter affects om companies progress
class WorldSituation():

	def __init__(self):
		self.military_points = 0
		self.food_points = 0
		self.scince_points = 0
		self.mining_points = 0

	def change_situation(self, changes):
		self.military_points += changes.military_points
		self.food_points += changes.food_points
		self.scince_points += changes.scince_points
		self.mining_points += changes.mining_points
