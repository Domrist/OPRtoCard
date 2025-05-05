from Upgrade import *
from contants import *

def correctHeaderWidth(a_fpdf, a_headerString):
	res = []
	print("HEADER STRING -> ", a_headerString, "\t", a_fpdf.get_string_width(a_headerString) + (a_fpdf.c_margin))
	if a_fpdf.get_string_width(a_headerString) > DEFAULT_CARD_WIDTH:
		print("HEADER MORE THAN ALLOWED")

	return res


class UpgradePage:

	upgradeHeaderLines : []
	upgrades : []

	def __init__(self, a_fpdf, a_headerData, a_upgradesData):

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

				correctHeaderWidth(a_fpdf, localUpradeHeaderObject["upgradeName"])
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
