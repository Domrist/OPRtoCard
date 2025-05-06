from contants import *
from UpgradePage import *


class UnitData:

	unitName : str
	quaDef : str
	keywords : []
	unitWeaponData : []

	upgradePages : []
	pageCapacity : int



	def __init__(self, a_name, a_quaDef, a_keywords, a_weaponData):
		self.unitName = a_name
		self.quaDef = a_quaDef
		self.keywords = a_keywords
		self.unitWeaponData = a_weaponData

		self.upgradePages = []
		self.pageCapacity = 1	# by default - by first face page



	def addUpgradePage(self, a_upgradePage):
		self.upgradePages.append(a_upgradePage)
		self.pageCapacity += a_upgradePage.getPagesCapacity()



	def getUnitDataPageCount(self):
		return self.pageCapacity



	def print(self):
		print(self.unitName)
		print(self.quaDef)
		print(self.keywords)
		print(self.unitWeaponData)

		for upgradePage in self.upgradePages:
			upgradePage.print()
		print("\n")



	def getUnitName(self):
		return self.unitName



	def getQuaDef(self):
		return self.quaDef



	def getKeywords(self):
		return self.keywords



	def getWeaponData(self):
		return self.unitWeaponData



	def getUpgradePages(self):
		return self.upgradePages
