from fpdf import FPDF

from contants import *
from Upgrade import *
from UpgradePage import *

from UnitData import *

from fpdf import FPDF

pdf = FPDF(orientation='L', unit='mm', format='A4')

def writeText(x,y,text, sizee = 10,  sstyle = ''):
	if sstyle:
		pdf.set_font(family = "Helvetica", style = sstyle, size = sizee)
	else:
		pdf.set_font(family = "Helvetica", size = sizee)

	pdf.set_xy(x,y)
	pdf.write(0,text)



def writeCenteredText(x,y,text,sizee=10):

	#print(pdf.c_margin)

	if x < 0:
		print("LESS")
	pdf.set_font(family = "Helvetica", size = sizee)
	textLength = pdf.get_string_width(text)

	x -= (textLength/2)

	x -= (pdf.c_margin)	# EVERY TEXT HAVE MARGIN

	pdf.set_xy(x,y)
	pdf.write(0,text)



def writeWeaponData(weaponObjects):
	localHeight = 30
	for weaponData in weaponObjects:
		weaponString = ""
		weaponSpecs = ""
		weaponName = weaponData["weaponName"]
		keyIterator = iter(weaponData)

		for key,valu in weaponData.items():
			if key == "weaponName":
				continue
			elif valu == "-":
				continue
			weaponSpecs += valu + ","
		writeText(0, localHeight, weaponName)
		localHeight += STEP_LINE_GLOBAL
		writeText(0, localHeight, "|-" + weaponSpecs)
		localHeight += STEP_LINE_GLOBAL



def getUnitWeaponData(a_weaponObjects):
	weaponDataArr = []
	for weaponData in a_weaponObjects:

		tmpWeaponData = {}
		weaponSpecs = ""
		weaponName = ""

		for key,valu in weaponData.items():
			if key == "weaponName":
				weaponName = weaponData["weaponName"]
				continue
			elif key == "weaponAP" and valu != "-":
				valu = "AP(" + valu + ")"
			elif valu == "-":
				continue
			weaponSpecs += valu + ","

		weaponSpecs = weaponSpecs[:-1]

		tmpWeaponData["WeaponName"] = weaponName
		tmpWeaponData["WeaponSpecs"] = weaponSpecs

		weaponDataArr.append(tmpWeaponData)

	return weaponDataArr



def getUpgradeRowCount(upgradeObject):
	res = 0
	updgradePageHeader = upgradeObject["key"]

	if AND_STRING in updgradePageHeader:
		splittedUpgradeHeader = updgradePageHeader.split(AND_STRING)

		for splittedUpgradeHdr in splittedUpgradeHeader:
			localUpradeLineObject = getSplittedUpgradesListPos(splittedUpgradeHdr)
			for item in localUpradeLineObject:
				upgradeName = item["upgradeName"]
				res += 1	# for upgrade name
				upgradeSpecs = splitStringToTriples(deleteFirstLastStaples(item["upgradeSpecs"]))
				res += len(upgradeSpecs)


		for upgradeLine in upgradeObject["value"]:
			tmpUpgradeLine = [var for var in upgradeLine.split("\n") if var]
			upgradeName = tmpUpgradeLine[0]
			upgradeCost = tmpUpgradeLine[1]

			tmpUpgrade = Upgrade(upgradeName, upgradeCost)

			res += tmpUpgrade.getTotalLineCapacity()

	else:
		pass

	return res



def writeUpdgrade(a_baseY, yPagePos, a_upgradePage):

	global GLOBAL_X_POS
	BASE_Y = a_baseY

	upgradeRowCount = a_upgradePage.getRowCount()

	pageToPrint = a_upgradePage

	cardRowBalance = DEFAULT_ROW_COUNT_PER_PAGE

	for headerString in pageToPrint.getHeaderData():
		writeText(GLOBAL_X_POS, yPagePos, headerString, 8, 'B')
		yPagePos += STEP_LINE_GLOBAL
		cardRowBalance -= 1

	pdf.line(GLOBAL_X_POS, yPagePos-2, GLOBAL_X_POS+40, yPagePos-2)

	for upgrade in pageToPrint.getUpgrades():

		if upgrade.getTotalLineCapacity() > cardRowBalance:
			GLOBAL_X_POS += DEFAULT_CARD_WIDTH
			cardRowBalance = DEFAULT_ROW_COUNT_PER_PAGE
			yPagePos = 4 + BASE_Y

		for upgradeLine in upgrade.getUpgradesLine():
			for upgradeLineString in upgradeLine.getData():
				writeText(GLOBAL_X_POS, yPagePos, upgradeLineString, 8)
				yPagePos += STEP_LINE_GLOBAL

		cardRowBalance -= upgrade.getTotalLineCapacity()
		pdf.line(GLOBAL_X_POS, yPagePos-2, GLOBAL_X_POS + 40, yPagePos-2)

	GLOBAL_X_POS += DEFAULT_CARD_WIDTH



def getUpgradePages(a_upgradeObject):
	tmpUpgrade = UpgradePage(a_upgradeObject["key"], a_upgradeObject["value"])
	return tmpUpgrade



def writeFillTest():
	heightShift = 4
	for i in range(DEFAULT_ROW_COUNT_PER_PAGE):
		writeText(40, heightShift, "Some nights expired",10)
		heightShift += STEP_LINE_GLOBAL



def initHerCardData(obj):

	tmpUnitName = obj["unitName"]
	tmpUnitQuaDef = obj["quadef"]


	keyWordsArr = []
	tripletsKeywords = splitStringToTriples2(obj["keywords"])
	for keywordTriplet in tripletsKeywords:
		tripletStr = fromTripletToString(keywordTriplet)
		keyWordsArr.append(tripletStr)

	# блок вывода текущего оружия
	tmpWeaponData = getUnitWeaponData(obj["weapon"])

	tmpUnitData = UnitData(tmpUnitName, tmpUnitQuaDef, keyWordsArr, tmpWeaponData)

	upgradeIndex = 0
	#for upgrade in range(len(obj["upgrades"])-1):
	for upgrade in obj["upgrades"]:
		tmpUpgrade = getUpgradePages(upgrade)
		tmpUnitData.addUpgradePage(tmpUpgrade)

	#print("TOTAL PAGE COUNT -> ", tmpUnitData.getUnitDataPageCount())

	return tmpUnitData



def writeHeroCardData(a_unitData, a_rowIndex):

	baseRowY = a_rowIndex * DEFAULT_CARD_HEIGHT

	global GLOBAL_X_POS

	GLOBAL_X_POS = 40

	headerYPos = ()

	writeCenteredText(20, 4 + baseRowY, a_unitData.getUnitName(), 9)
	writeCenteredText(20, DEFAULT_ROW_COUNT_PER_PAGE + baseRowY, a_unitData.getQuaDef(), 14)

	pdf.line(0, 15 + baseRowY, 40, 15 + baseRowY)

	# генерация кейвордов
	heightShift = 20 + baseRowY

	for keywordTriplet in a_unitData.getKeywords():
		writeCenteredText(20, heightShift, keywordTriplet, 8)
		heightShift += STEP_LINE_GLOBAL

	for weaponData in a_unitData.getWeaponData():
		writeText(0, heightShift, weaponData["WeaponName"], 8)
		heightShift += STEP_LINE_GLOBAL
		writeText(0, heightShift, weaponData["WeaponSpecs"], 8)
		heightShift += STEP_LINE_GLOBAL

	# блок вывода страниц улучшений
	for upgrade in a_unitData.getUpgradePages():
		writeUpdgrade(baseRowY, 4 + baseRowY, upgrade)
