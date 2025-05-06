from UpgradeLine import *
from contants import *

class Upgrade:

	upgradesLine : []
	cost : int
	totalLineCapacity : int

	def __init__(self, a_parsedString, a_cost):

		self.upgradesLine = []
		self.cost = a_cost
		self.totalLineCapacity = 0

		splittedUpgrades = getSplittedUpgradesListPos(a_parsedString)

		#print("Upgrade -> parsed string -> ", splittedUpgrades)

		for upgradeData in splittedUpgrades:
			self.upgradesLine.append(UpgradeLine(upgradeData["upgradeName"], upgradeData["upgradeSpecs"]))

		for line in self.upgradesLine:
			self.totalLineCapacity += line.getLineCapacity()



	def getTotalLineCapacity(self):
		return self.totalLineCapacity



	def getUpgradesLine(self):
		return self.upgradesLine



	def print(self):
		print("UPGRADE")
		for upLine in self.upgradesLine:
			upLine.print()
		print("\n")
