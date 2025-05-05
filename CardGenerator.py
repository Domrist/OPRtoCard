from fpdf import FPDF

from contants import *
from Upgrade import *
from UpgradePage import *

from fpdf import FPDF

pdf = FPDF(orientation='L', unit='mm', format='A4')

def writeText(x,y,text, sizee = 10,  sstyle = ''):
	if sstyle:
		pdf.set_font(family = "Helvetica", style = sstyle, size = sizee)
	else:
		pdf.set_font(family = "Helvetica", size = sizee)
	textLength = pdf.get_string_width(text)
	textLength = textLength/2
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
		print(weaponData.items())
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



def getHeaderWriteData(a_incomingStr):
	res = []
	updgradePageHeader = a_incomingStr

	return res




def writeUpdgrade(xPagePos, yPagePos, upgradeObject):

	global GLOBAL_X_POS

	upgradeRowCount = getUpgradeRowCount(upgradeObject)

	if upgradeRowCount > DEFAULT_ROW_COUNT_PER_PAGE:
		print("SHOULD WRITE WITH MINIMUM 2 PAGES")
	else:
		print("CAN FIT ALL DATA INSIDE ONE PAGE")

	pageToPrint = UpgradePage(upgradeObject["key"], upgradeObject["value"])

	cardRowBalance = DEFAULT_ROW_COUNT_PER_PAGE

	for headerString in pageToPrint.getHeaderData():
		writeText(GLOBAL_X_POS, yPagePos, headerString, 8, 'B')
		yPagePos += STEP_LINE_GLOBAL
		cardRowBalance -= 1

	pdf.line(GLOBAL_X_POS, yPagePos-2, xPagePos+40, yPagePos-2)

	for upgrade in pageToPrint.getUpgrades():

		if upgrade.getTotalLineCapacity() > cardRowBalance:
			GLOBAL_X_POS += DEFAULT_CARD_WIDTH
			cardRowBalance = DEFAULT_ROW_COUNT_PER_PAGE
			yPagePos = 4

		for upgradeLine in upgrade.getUpgradesLine():
			for upgradeLineString in upgradeLine.getData():
				writeText(GLOBAL_X_POS, yPagePos, upgradeLineString, 8)
				yPagePos += STEP_LINE_GLOBAL

		cardRowBalance -= upgrade.getTotalLineCapacity()
		pdf.line(GLOBAL_X_POS, yPagePos-2, GLOBAL_X_POS + 40, yPagePos-2)

	GLOBAL_X_POS += DEFAULT_CARD_WIDTH



def writeFillTest():
	heightShift = 4
	for i in range(DEFAULT_ROW_COUNT_PER_PAGE):
		writeText(40, heightShift, "Some nights expired",10)
		heightShift += STEP_LINE_GLOBAL



def initHerCardData(obj):

	#writeText(0,5,obj["unitName"])
	writeCenteredText(20,4,obj["unitName"], 9)
	writeCenteredText(20, DEFAULT_ROW_COUNT_PER_PAGE,obj["quadef"],14)

	pdf.line(0,15,40,15)

	# генерация кейвордов
	heightShift = 20

	tripletsKeywords = splitStringToTriples2(obj["keywords"])
	for keywordTriplet in tripletsKeywords:
		print(keywordTriplet)
		tripletStr = fromTripletToString(keywordTriplet)
		writeCenteredText(20, heightShift, tripletStr, 8)
		heightShift += STEP_LINE_GLOBAL

	heightShift += STEP_LINE_GLOBAL

	# блок вывода текущего оружия
	writeWeaponData(obj["weapon"])

	# блок вывода страниц улучшений
	#writeFillTest()

	upgradeIndex = 0
	for upgrade in obj["upgrades"]:
		writeUpdgrade(0, 4, obj["upgrades"][upgradeIndex])
		upgradeIndex += 1
