import random
import time
from uuid import uuid4

from companies.company_data import CompanyData

company_type=("Forge","Quarry","Sawmill", "Mill", "Farm", "Alchemistry", "Pharmacy", "Jewellery")
owner_name=('Leidron Endas','Shrierpuld Fihlusols','Zhanreir Talmirnord', 'Krelul Keva', 'Linbak Denma', "Samneld Grunholz", "Kircard Bamberg", "Dudrik Steinlich")

# Operate with company
class Company():

	cost_last_update_time = 0.0
	cost_next_update_time = 0.0

	@property
	def name(self):
		return self.data.name
	@property
	def uuid(self):
		return self.data.uuid
	@property
	def cost(self):
		return self.data.cost
	

	def __init__(self):
		# Create data object
		self.data = CompanyData()

		# Generate name
		random.seed(time.time())
		self.data.name = random.choice(company_type) + " of " + random.choice(owner_name)

		# Generate uniq id.
		# TODO : verify, that this is right solution
		self.data.uuid = str(uuid4())

		# Generate started cost
		random.seed(time.time())
		random_cost = random.uniform(10.0, 30.0)
		self.data.cost = round(random_cost,2)

		# Set next cost update time
		self.cost_last_update_time = time.time()
		self.generate_next_cost_update_time_random()

	def generate_next_cost_update_time_random(self):
		# Generate next time for update
		random.seed(time.time())
		period = random.uniform(5.0, 7.0)
		period = round(period,2)
		self.cost_next_update_time = self.cost_last_update_time + period

	def generate_random_cost(self):
		# Generate random value for change cost
		current_time = time.time()
		random.seed(current_time)
		diff = random.uniform(-0.5, 1.0)
		diff = round(diff,2)
		self.data.cost += diff
		self.cost_last_update_time  = current_time


