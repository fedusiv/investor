from enum import Enum

# This type represent in what stage company is now
# None means, company is not initialized properly or it has no stocks
# Open means, that everyone can buy stocks
# Closed means, that company is kind on investing process, and only few users can buy it
class CompanyType(Enum):
	NONE = 0
	OPEN = 1
	CLOSED = 2

class CompanyBusinessType(Enum):
	MILITARY = 1
	FOOD = 2
	SCINCE = 3
	MINING = 4