COMMA = ","

STEP_8_MULT_045 = 8 * 0.45
STEP_8_MULT_05 = 8 * 0.5
STEP_LINE_GLOBAL = STEP_8_MULT_05
AND_STRING = " and "
DEFAULT_ROW_COUNT_PER_PAGE = 12 # При стандартном размере шрифта в размере 8
DEFAULT_CARD_WIDTH = 40 # in mm

GLOBAL_X_POS = 40	# MUTABLE

def getSplittedUpgradesListPos(st):
	st += ","
	counter = 0
	pos = 0
	res = []
	lowestPos = 0

	tmpText = "("
	if tmpText not in st:
		st = st[:-1]
		tmpObject = {}
		tmpObject["upgradeName"] = st
		tmpObject["upgradeSpecs"] = ""
		res.append(tmpObject)
		return res

	for i in st:
		if i == "(":
			counter += 1
		elif i == ")":
			counter -= 1
		if counter == 0 and i == ",":

			tmpUpgradeLine = st[lowestPos:pos]
			ccounter = 0
			lSignCounter = 0
			for x in tmpUpgradeLine:
				if x == "(" and lSignCounter == 0:
					tmpObject = {}
					lSignCounter += 1
					if COMMA in tmpUpgradeLine:
						tmpObject["upgradeName"] = tmpUpgradeLine[:ccounter-1]
					else:
						tmpObject["upgradeName"] = tmpUpgradeLine[:ccounter]
					tmpObject["upgradeSpecs"] = tmpUpgradeLine[ccounter:]
					res.append(tmpObject)
				ccounter += 1
			lowestPos = pos+2
		pos += 1
	return res



def deleteFirstLastStaples(a_str):
	a_str = a_str[1:]
	a_str = a_str[:-1]
	return a_str



def splitStringToTriples(a_incomingString, a_divider = ","):
	res = []
	counter = 0
	preparesString = a_incomingString.split(a_divider)

	localArray = []
	for i in preparesString:
		if preparesString[counter]:
			localArray.append(preparesString[counter])
		counter += 1
		if counter == 3 or counter == len(preparesString):
			if localArray:
				res.append(localArray)

			localArray = []
			counter = 0
	return res



def splitStringToTriples2(a_incomingString, a_divider = ","):
	res = []
	counter = 0
	preparesString = a_incomingString.split(a_divider)

	localArray = []

	index = 0

	for i in preparesString:

		if preparesString[counter]:
			localArray.append(preparesString[index])
		counter += 1
		index += 1

		if counter == 3 or index == (len(preparesString)):
			res.append(localArray)
			localArray = []
			counter = 0
	return res



def fromTripletToString(a_triplet):
	str = ""

	for tripletElement in a_triplet:
		str += tripletElement + ","

	str = str[:-1]

	return str


