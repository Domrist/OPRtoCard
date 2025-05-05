from Upgrade import *
from contants import *

class UpgradePage:

	upgradeHeaderLines : []
	upgrades : []

	def __init__(self, a_headerData, a_upgradesData):

		self.upgradeHeaderLines = []
		self.upgrades = []

		if AND_STRING in a_headerData:

			splittedUpgradeHeader = a_headerData.split(AND_STRING)

			for splittedUpgradeHdr in splittedUpgradeHeader:

				localUpradeLineObject = getSplittedUpgradesListPos(splittedUpgradeHdr)

				for item in localUpradeLineObject:
					self.upgradeHeaderLines.append(item['upgradeName'])
					for triplet in splitStringToTriples(item['upgradeSpecs']):
						tripletStr = fromTripletToString(triplet)
						self.upgradeHeaderLines.append(tripletStr)
		else:
			for localUpradeHeaderObject in getSplittedUpgradesListPos(a_headerData):
				self.upgradeHeaderLines.append(localUpradeHeaderObject["upgradeName"])
				self.upgradeHeaderLines.append(localUpradeHeaderObject["upgradeSpecs"])	# should breack to triples!!!


		for upgradeLine in a_upgradesData:
			tmpUpgradeLine = [var for var in upgradeLine.split("\n") if var]
			upgradeName = tmpUpgradeLine[0]
			upgradeCost = tmpUpgradeLine[1]

			self.upgrades.append(Upgrade(upgradeName, upgradeCost))



	def print(self):
		print(self.upgradeHeaderLines)
		for up in self.upgrades:
			up.print()



	def getHeaderData(self):
		return self.upgradeHeaderLines



	def getUpgrades(self):
		return self.upgrades
