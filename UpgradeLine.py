from contants import *


class UpgradeLine:

	lineCapacity : int
	caption : str
	upgrades : []

	def __init__(self, a_caption, a_upgrades):
		self.lineCapacity = 0
		self.upgrades = []
		self.caption = a_caption

		self.lineCapacity += 1	#	for caption

		splittedTripples = splitStringToTriples(deleteFirstLastStaples(a_upgrades))

		for tripple in splittedTripples:
			stringifyTriple = fromTripletToString(tripple)
			self.upgrades.append(stringifyTriple)
			self.lineCapacity += 1	# for every triples



	def getLineCapacity(self):
		return self.lineCapacity



	def getData(self):
		res = []

		res.append(self.caption)
		res += self.upgrades

		return res



	def print(self):
		print(self.caption, " : ", self.upgrades)
