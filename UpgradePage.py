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

	rowCapacity : int

	pagesCapacity : int

	def __init__(self, a_headerData, a_upgradesData):

		self.upgradeHeaderLines = []
		self.upgrades = []
		self.rowCapacity = 0
		self.pagesCapacity = 0

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

		self.rowCapacity += len(self.upgradeHeaderLines)

		for upgradeLine in a_upgradesData:

			tmpUpgradeLine = [var for var in upgradeLine.split("\n") if var]

			upgradeName = tmpUpgradeLine[0]
			upgradeCost = tmpUpgradeLine[1]

			tmpUpgrade = Upgrade(upgradeName, upgradeCost)

			self.upgrades.append(tmpUpgrade)
			self.rowCapacity += tmpUpgrade.getTotalLineCapacity()

		if self.rowCapacity <= 12:
			self.pagesCapacity = 1
		else:
			self.pagesCapacity = int(self.rowCapacity / DEFAULT_ROW_COUNT_PER_PAGE)
			if int(self.rowCapacity % DEFAULT_ROW_COUNT_PER_PAGE) != 0:
				self.pagesCapacity += 1



	def print(self):
		print(self.upgradeHeaderLines)
		for up in self.upgrades:
			up.print()



	def getHeaderData(self):
		return self.upgradeHeaderLines



	def getUpgrades(self):
		return self.upgrades



	def getPagesCapacity(self):
		return self.pagesCapacity



	def getRowCount(self):
		return self.rowCapacity
