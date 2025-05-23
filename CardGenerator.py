from fpdf import FPDF

from contants import *
from UnitData import *


class CardGenerator:

	pdf : FPDF
	yRowScalerPerPage : int

	def __init__(self, a_fpdf):
		self.pdf = a_fpdf
		self.yRowScalerPerPage = 0



	def writeText(self, x, y, text, sizee = 10,  sstyle = ''):
		if sstyle:
			self.pdf.set_font(family = "Helvetica", style = sstyle, size = sizee)
		else:
			self.pdf.set_font(family = "Helvetica", size = sizee)

		self.pdf.set_xy(x,y)
		self.pdf.write(0,text)



	def writeCenteredText(self, x, y, text, sizee=10):
		if x < 0:
			# we should throw error
			pass
		self.pdf.set_font(family = "Helvetica", size = sizee)
		textLength = self.pdf.get_string_width(text)

		x -= (textLength/2)

		x -= (self.pdf.c_margin)	# EVERY TEXT HAVE MARGIN

		self.pdf.set_xy(x,y)
		self.pdf.write(0,text)



	def getTextWidth(self, a_text, a_textSize = 10):
		self.pdf.set_font(family = "Helvetica", size = a_textSize)
		textLength = self.pdf.get_string_width(a_text)
		textLength += (self.pdf.c_margin * 2)
		return textLength



	def fillTest(self):
		sss = "0123456789"
		self.writeText(40, 4, sss, 10)



	def splitSingleGainWithBraces(self, a_string):

		tmpArr = []
		if "(" not in a_string:
			return []

		index = a_string.index("(")
		splittedName = a_string[:index]
		splittedUpgrade = a_string[index:]

		# LATER REWRITE THAT STUFF
		if splittedUpgrade[0] == "(" and splittedUpgrade[-1] == ")":
			tmpArr = [splittedName, splittedUpgrade]
		else:
			splittedUpgrade = "(" + splittedUpgrade + ")"
			tmpArr = [splittedName, splittedUpgrade]

		return tmpArr



	# разделение строки типап 'Ap(1), Fast, Blast(5), Furios' на массив типа [ 'Ap(1)', 'Fast', 'Blast(5)', 'Furios']
	def splitStringByTopLevelBraces(self, a_string):
		arr = []

		counter = 0
		lowerBorder = 0
		higherBorder = 0

		for i in a_string:
			higherBorder += 1
			if i == "(":
				counter += 1
			elif i == ")":
				counter -= 1
			elif i == "," and counter == 0:
				arr.append(a_string[lowerBorder:higherBorder-1])
				lowerBorder = higherBorder

			if higherBorder == len(a_string):
				arr.append(a_string[lowerBorder:higherBorder])

		return arr


	# превращение строки типа 'Realm Lord(Private Guard(Men-at-Arms(Realm Lord(Private Guard( AP(1), Men-at-Arms)))))' в удобную для обхода структуру
	def getGetCollectionFromNestedString(self, a_string):

		objectToModify = {}

		objectToModify["nodeCaption"] = ""
		objectToModify["nodeChilds"] = []
		objectToModify["nodeValues"] = []

		if a_string.count("(") == 0:	# Fast/Hero/etc

			objectToModify["nodeCaption"] = a_string
			return objectToModify

		else:

			objectToModify["nodeCaption"] = a_string[:a_string.find("(")]

			nextStringParse = a_string[a_string.find("(") + 1:a_string.rfind(")")]

			for item in self.splitStringByTopLevelBraces(nextStringParse):
				if item.count("(") == 1 and item.count(")") == 1:

					tmpObject = {}
					tmpObject["nodeChilds"] = []
					tmpObject["nodeCaption"] = item[:item.find("(")]
					tmpObject["nodeValues"] = []
					tmpObject["nodeValues"].append(item[item.find("(")+1:item.find(")")])

					objectToModify["nodeChilds"].append(tmpObject)
				else:

					obj = self.getGetCollectionFromNestedString(item)
					objectToModify["nodeChilds"].append(obj)

			return objectToModify

		return objectToModify



	def appendObjectFromNestedCollectionToArray(self, a_obj, a_arr, a_recursionLevel = 0):

		localRecursionLevel = a_recursionLevel

		appendedString = ""
		if a_recursionLevel != 0:
			appendedString = "|"

		a_arr.append(appendedString + ("-" * a_recursionLevel) + a_obj["nodeCaption"])

		if len(a_obj["nodeValues"]) == 1:
			if self.getTextWidth( ("{0}({1})").format(a_arr[-1], a_obj["nodeValues"][0]), 8) > (DEFAULT_CARD_WIDTH - 10):
				a_arr.append(appendedString + ("-" * (a_recursionLevel + 1)) + a_obj["nodeValues"][0])
			else:
				a_arr[-1] = ("{0}({1})").format(a_arr[-1], a_obj["nodeValues"][0])
		else:
			for nodeValue in a_obj["nodeValues"]:
				a_arr.append(appendedString + ("-" * (a_recursionLevel+1)) + str(nodeValue))


		for child in a_obj["nodeChilds"]:
			self.appendObjectFromNestedCollectionToArray(child, a_arr, localRecursionLevel + 1)

		return a_arr



	### API DATA WRITER
	def writeFirstHeroCardData(self, a_unitData):

		baseRowY = self.yRowScalerPerPage * DEFAULT_CARD_HEIGHT

		global GLOBAL_X_POS

		GLOBAL_X_POS = 40

		# UNIT NAME
		self.writeCenteredText(20, 4 + baseRowY, a_unitData["name"], 9)

		# QUA - DEF
		with self.pdf.local_context(text_mode = 2, line_width=0):
			self.pdf.set_text_color(255, 50, 15)
			self.writeCenteredText(20, DEFAULT_ROW_COUNT_PER_PAGE + baseRowY, a_unitData["quaDef"], 14)


		self.pdf.line(0, 15 + baseRowY, 40, 15 + baseRowY)

		# запись кейвордов
		heightShift = 20 + baseRowY

		if len(a_unitData["unitTrinkets"]) != 0:
			unitTrinketCollection = self.splitStringByTopLevelBraces(a_unitData["unitTrinkets"][0])
			trinketIndex = len(unitTrinketCollection)

			while len(unitTrinketCollection) > 0:
				strToCompare = ",".join(unitTrinketCollection[:trinketIndex])

				if self.getTextWidth(strToCompare, 8) > DEFAULT_CARD_WIDTH - 3:
					trinketIndex -= 1
					continue

				self.writeCenteredText(20, heightShift, strToCompare, 8)
				heightShift += STEP_LINE_GLOBAL
				unitTrinketCollection = unitTrinketCollection[trinketIndex:]
				trinketIndex = len(unitTrinketCollection)

		# запись оружия

		for weaponData in a_unitData["weaponsData"]:
			self.writeText(0, heightShift, weaponData["weaponName"], 8)
			heightShift += STEP_LINE_GLOBAL
			for weaponTrinketsLine in weaponData["trinkets"]:
				self.writeText(0, heightShift, weaponTrinketsLine, 8)
				heightShift += STEP_LINE_GLOBAL



	def writeSingleLineSpecRules(self, a_option, a_gain, a_gainIndex, a_tmpCost, a_position, a_makeStepFunction, a_writePointsFunction):
		stringToWrite = a_gain["gainName"] + "(" + a_gain["gainSpecRule"][0] + ")"
		if len(stringToWrite) > MAX_STRING_LENGTH:

			obj = self.getGetCollectionFromNestedString(stringToWrite)
			tmpArr = []

			if self.getTextWidth(a_gain["gainSpecRule"][0], 8) > (DEFAULT_CARD_WIDTH-10):
				self.appendObjectFromNestedCollectionToArray(obj, tmpArr)

			for st in range(len(tmpArr)):

				self.writeText(a_position.x, a_position.y, tmpArr[st], 8)

				if st == (len(tmpArr)-1) and a_gainIndex == len(a_option["gains"]) -1:
					a_writePointsFunction(a_tmpCost, a_position.x, a_position.y)
				a_makeStepFunction()
		else:
			self.writeText(a_position.x, a_position.y, stringToWrite, 8)
			a_writePointsFunction(a_tmpCost, a_position.x, a_position.y)
			a_makeStepFunction()



	def getSingleLineSpecRulesCollection(self, a_option, a_gain, a_gainIndex, a_tmpCost):

		res = []

		stringToWrite = a_gain["gainName"] + "(" + a_gain["gainSpecRule"][0] + ")"
		if len(stringToWrite) > MAX_STRING_LENGTH:

			obj = self.getGetCollectionFromNestedString(stringToWrite)
			tmpArr = []

			if self.getTextWidth(a_gain["gainSpecRule"][0], 8) > (DEFAULT_CARD_WIDTH-10):
				self.appendObjectFromNestedCollectionToArray(obj, tmpArr)

			res = tmpArr

		else:
			#self.writeText(a_position.x, a_position.y, stringToWrite, 8)
			res.append(stringToWrite)

		return res



	# writeTripletsSpecRules
	def writeTripletsSpecRules(self, a_option, a_gain, a_gainIndex, a_tmpCost, a_position, a_makeStepFunction, a_writePointsFunction):
		stringToWrite = a_gain["gainName"]
		self.pdf.set_text_color(0)
		self.writeText(a_position.x, a_position.y, stringToWrite, 8)
		self.pdf.set_text_color(0)
		a_makeStepFunction()

		finalTriples = []

		triples = fromCollectionToStringifyTriplets(a_gain["gainSpecRule"])

		gainSpecs = a_gain["gainSpecRule"]

		index = len(gainSpecs)

		while len(gainSpecs) != 0:
			st = ",".join(gainSpecs[:index])

			if self.getTextWidth(st, 8) > (DEFAULT_CARD_WIDTH-10):
				index -= 1
			else:
				finalTriples.append(st)
				gainSpecs = gainSpecs[index:]
				index = len(gainSpecs)


		for tripleIndex in range(len(finalTriples)):
			stringToWrite = finalTriples[tripleIndex]

			self.pdf.set_text_color(128)
			self.writeText(a_position.x, a_position.y, stringToWrite, 8)
			self.pdf.set_text_color(0)

			if tripleIndex == (len(finalTriples)-1) and a_gainIndex == (len(a_option["gains"]) -1):
				a_writePointsFunction(a_tmpCost, a_position.x, a_position.y)
			a_makeStepFunction()



	# getTripletsSpecRules
	def getTripletsSpecRules(self, a_option, a_gain, a_gainIndex, a_tmpCost):

		res = []

		stringToWrite = a_gain["gainName"]
		#self.pdf.set_text_color(0)
		#self.writeText(a_position.x, a_position.y, stringToWrite, 8)
		res.append(stringToWrite)
		#self.pdf.set_text_color(0)
		#a_makeStepFunction()

		finalTriples = []

		triples = fromCollectionToStringifyTriplets(a_gain["gainSpecRule"])

		gainSpecs = a_gain["gainSpecRule"]

		index = len(gainSpecs)

		while len(gainSpecs) != 0:
			st = ",".join(gainSpecs[:index])

			if self.getTextWidth(st, 8) > (DEFAULT_CARD_WIDTH-10):
				index -= 1
			else:
				finalTriples.append(st)
				gainSpecs = gainSpecs[index:]
				index = len(gainSpecs)

		res = finalTriples

		'''
		for tripleIndex in range(len(finalTriples)):
			stringToWrite = finalTriples[tripleIndex]

			#self.pdf.set_text_color(128)
			#self.writeText(a_position.x, a_position.y, stringToWrite, 8)
			res.append(stringToWrite)
			#self.pdf.set_text_color(0)

			if tripleIndex == (len(finalTriples)-1) and a_gainIndex == (len(a_option["gains"]) -1):
				#a_writePointsFunction(a_tmpCost, a_position.x, a_position.y)
		'''

		return res



	# writeUpgradeHeroData
	def writeUpgradeHeroData(self, a_upgrade, a_position):

		cardRowBalance = DEFAULT_ROW_COUNT_PER_PAGE

		upgrade = a_upgrade

		def checkEndPage():
			nonlocal cardRowBalance
			if cardRowBalance <= 0:
				cardRowBalance = DEFAULT_ROW_COUNT_PER_PAGE
				a_position.y = NAME_TOP_MARGIN + DEFAULT_CARD_HEIGHT * self.yRowScalerPerPage
				a_position.x += DEFAULT_CARD_WIDTH


		def makeRowStep(a_isFinalRowStep = -1):
			nonlocal cardRowBalance

			a_position.y += STEP_LINE_GLOBAL
			if a_isFinalRowStep != -1:
				a_position.y += a_isFinalRowStep

			cardRowBalance -= 1


		def makeStep(a_isFinalRowStep = -1):
			makeRowStep(a_isFinalRowStep)
			checkEndPage()


		def goToNextPage():
			nonlocal cardRowBalance
			a_position.y = NAME_TOP_MARGIN + DEFAULT_CARD_HEIGHT * self.yRowScalerPerPage
			a_position.x += DEFAULT_CARD_WIDTH


		def writePoints(a_cost, a_x, a_y):
			localTextWidth = self.getTextWidth( str(a_cost)+ "pts", 8)
			textXPos = a_x + DEFAULT_CARD_WIDTH - (localTextWidth)
			self.writeText(textXPos, a_y, str(a_cost) + "pts", 8)



		# print header data

		headerTextFontSize = 8
		self.pdf.set_font(family = "Helvetica", style = "B", size = headerTextFontSize)

		headerStrings = []
		if AND_STRING in upgrade["upgradeName"]:
			headerStrings = upgrade["upgradeName"].split(AND_STRING)
			headerStrings[1] = AND_STRING + " " + headerStrings[1]
			headerStrings[1] = headerStrings[1][1:]
		else:
			while self.getTextWidth(upgrade["upgradeName"], headerTextFontSize) > (DEFAULT_CARD_WIDTH - self.pdf.c_margin*2):
				headerTextFontSize -= 1
				self.pdf.set_font(family = "Helvetica", style = "B", size = headerTextFontSize)
			headerStrings.append(upgrade["upgradeName"])


		for headerStringIndex in range(len(headerStrings)):
			self.writeText(a_position.x, a_position.y, headerStrings[headerStringIndex], headerTextFontSize, 'B')
			makeStep()

		# end print header data

		#####

		for iOption in upgrade["options"]:
			tmpCost = iOption["cost"]

			for gainEnumerate in enumerate(iOption["gains"]):

				gain = gainEnumerate[1]
				gainIndex = gainEnumerate[0]

				specRulesLen = len(gain["gainSpecRule"])

				if specRulesLen == 1:	# should print at same line as upgrade name
					self.writeSingleLineSpecRules(iOption, gain, gainIndex, tmpCost, a_position, makeStep, writePoints)
				elif specRulesLen >= 2:	### should be check for triplets length
					self.writeTripletsSpecRules(iOption, gain, gainIndex, tmpCost, a_position, makeStep, writePoints)

				elif specRulesLen == 0:
					stringToWrite = gain["gainName"]
					self.writeText(a_position.x, a_position.y, stringToWrite, 8)
					writePoints(tmpCost, a_position.x, a_position.y)
					makeStep()


			self.pdf.line(a_position.x + 2, a_position.y - 2, a_position.x + 38, a_position.y - 2)

		goToNextPage()
		# end write gains - and also end write of upgrade



	def increaseRowScaler(self):
		self.yRowScalerPerPage += 1



	def resetRowScaler(self):
		self.yRowScalerPerPage = 0



### append data to  unit data ###

# da first - fill header data


	def fillUnitFirstPageWithData(self, a_unitContainer, a_unitData):

		# UNIT NAME
		a_unitContainer.firstPageStringCollection["unitName"] = a_unitData["name"]

		# QUA - DEF
		a_unitContainer.firstPageStringCollection["quadef"] = a_unitData["quaDef"]

		# запись кейвордов
		tmpKeywords = []

		if len(a_unitData["unitTrinkets"]) != 0:
			unitTrinketCollection = self.splitStringByTopLevelBraces(a_unitData["unitTrinkets"][0][:])
			trinketIndex = len(unitTrinketCollection)

			while len(unitTrinketCollection) > 0:
				strToCompare = ",".join(unitTrinketCollection[:trinketIndex])

				if self.getTextWidth(strToCompare, 8) > DEFAULT_CARD_WIDTH - 3:
					trinketIndex -= 1
					continue

				tmpKeywords.append(strToCompare)
				unitTrinketCollection = unitTrinketCollection[trinketIndex:]
				trinketIndex = len(unitTrinketCollection)

		a_unitContainer.firstPageStringCollection["keywords"] = tmpKeywords

		# запись оружия

		tmpWeapons = []

		for weaponData in a_unitData["weaponsData"].copy():
			tmpWeapons.append(weaponData["weaponName"])
			for weaponTrinketsLine in weaponData["trinkets"]:
				tmpWeapons.append(weaponTrinketsLine)

		a_unitContainer.firstPageStringCollection["weapons"] = tmpWeapons



	def writeFirstPageByCardData(self, a_cardData):

		innerCardData = a_cardData.firstPageStringCollection

		baseRowY = self.yRowScalerPerPage * DEFAULT_CARD_HEIGHT

		global GLOBAL_X_POS

		GLOBAL_X_POS = 40

		# UNIT NAME
		self.writeCenteredText(20, 4 + baseRowY, innerCardData["unitName"], 9)

		# QUA - DEF
		with self.pdf.local_context(text_mode = 2, line_width=0):
			self.pdf.set_text_color(255, 50, 15)
			self.writeCenteredText(20, DEFAULT_ROW_COUNT_PER_PAGE + baseRowY, innerCardData["quadef"], 14)


		self.pdf.line(0, 15 + baseRowY, 40, 15 + baseRowY)

		# запись кейвордов
		heightShift = 20 + baseRowY

		for keywordLine in innerCardData["keywords"]:
			self.writeCenteredText(20, heightShift, keywordLine, 8)
			heightShift += STEP_LINE_GLOBAL


		# запись оружия

		for weaponLine in innerCardData["weapons"]:
			self.writeText(0, heightShift, weaponLine, 8)
			heightShift += STEP_LINE_GLOBAL

		# for weaponData in a_unitData["weaponsData"]:
		# 	self.writeText(0, heightShift, weaponData["weaponName"], 8)
		# 	heightShift += STEP_LINE_GLOBAL
		# 	for weaponTrinketsLine in weaponData["trinkets"]:
		# 		self.writeText(0, heightShift, weaponTrinketsLine, 8)
		# 		heightShift += STEP_LINE_GLOBAL



# da second - fill upgrades data


	def fillUnitUpgradeWithData(self, a_unitContainer, a_upgrade):

		cardRowBalance = DEFAULT_ROW_COUNT_PER_PAGE

		upgrade = a_upgrade.copy()

		# get header data

		headerTextFontSize = 8

		headerStrings = []

		if AND_STRING in upgrade["upgradeName"]:
			headerStrings = upgrade["upgradeName"].split(AND_STRING)
			headerStrings[1] = AND_STRING + " " + headerStrings[1]
			headerStrings[1] = headerStrings[1][1:]
		else:
			while self.getTextWidth(upgrade["upgradeName"], headerTextFontSize) > (DEFAULT_CARD_WIDTH - self.pdf.c_margin*2):
				headerTextFontSize -= 1
				self.pdf.set_font(family = "Helvetica", style = "B", size = headerTextFontSize)
			headerStrings.append(upgrade["upgradeName"])

		# end get header data

		#####

		res = []

		for iOption in upgrade["options"]:
			tmpCost = iOption["cost"]

			for gainEnumerate in enumerate(iOption["gains"]):

				gain = gainEnumerate[1]
				gainIndex = gainEnumerate[0]

				specRulesLen = len(gain["gainSpecRule"])

				if specRulesLen == 1:	# should print at same line as upgrade name
					#self.writeSingleLineSpecRules(iOption, gain, gainIndex, tmpCost, a_position, makeStep, writePoints)
					res += self.getSingleLineSpecRulesCollection(iOption, gain, gainIndex, tmpCost)
				elif specRulesLen >= 2:	### should be check for triplets length
					#self.writeTripletsSpecRules(iOption, gain, gainIndex, tmpCost, a_position, makeStep, writePoints)
					res += self.getTripletsSpecRules(iOption, gain, gainIndex, tmpCost)
				elif specRulesLen == 0:
					#stringToWrite = gain["gainName"]
					res.append(gain["gainName"])
					#self.writeText(a_position.x, a_position.y, stringToWrite, 8)
					#writePoints(tmpCost, a_position.x, a_position.y)


		# end write gains - and also end write of upgrade

		a_unitContainer.addGains( {"upgradeHeader" : headerStrings, "upgradeContent" : res} )



	def writeFirstPageByCardData(self, a_unitContainer):
		cardRowBalance = DEFAULT_ROW_COUNT_PER_PAGE

		upgrade = a_upgrade

		def checkEndPage():
			nonlocal cardRowBalance
			if cardRowBalance <= 0:
				cardRowBalance = DEFAULT_ROW_COUNT_PER_PAGE
				a_position.y = NAME_TOP_MARGIN + DEFAULT_CARD_HEIGHT * self.yRowScalerPerPage
				a_position.x += DEFAULT_CARD_WIDTH


		def makeRowStep(a_isFinalRowStep = -1):
			nonlocal cardRowBalance

			a_position.y += STEP_LINE_GLOBAL
			if a_isFinalRowStep != -1:
				a_position.y += a_isFinalRowStep

			cardRowBalance -= 1


		def makeStep(a_isFinalRowStep = -1):
			makeRowStep(a_isFinalRowStep)
			checkEndPage()


		def goToNextPage():
			nonlocal cardRowBalance
			a_position.y = NAME_TOP_MARGIN + DEFAULT_CARD_HEIGHT * self.yRowScalerPerPage
			a_position.x += DEFAULT_CARD_WIDTH


		def writePoints(a_cost, a_x, a_y):
			localTextWidth = self.getTextWidth( str(a_cost)+ "pts", 8)
			textXPos = a_x + DEFAULT_CARD_WIDTH - (localTextWidth)
			self.writeText(textXPos, a_y, str(a_cost) + "pts", 8)



		# print header data

		headerTextFontSize = 8
		self.pdf.set_font(family = "Helvetica", style = "B", size = headerTextFontSize)

		headerStrings = []
		if AND_STRING in upgrade["upgradeName"]:
			headerStrings = upgrade["upgradeName"].split(AND_STRING)
			headerStrings[1] = AND_STRING + " " + headerStrings[1]
			headerStrings[1] = headerStrings[1][1:]
		else:
			while self.getTextWidth(upgrade["upgradeName"], headerTextFontSize) > (DEFAULT_CARD_WIDTH - self.pdf.c_margin*2):
				headerTextFontSize -= 1
				self.pdf.set_font(family = "Helvetica", style = "B", size = headerTextFontSize)
			headerStrings.append(upgrade["upgradeName"])


		for headerStringIndex in range(len(headerStrings)):
			self.writeText(a_position.x, a_position.y, headerStrings[headerStringIndex], headerTextFontSize, 'B')
			makeStep()

		# end print header data

		#####

		for iOption in upgrade["options"]:
			tmpCost = iOption["cost"]

			for gainEnumerate in enumerate(iOption["gains"]):

				gain = gainEnumerate[1]
				gainIndex = gainEnumerate[0]

				specRulesLen = len(gain["gainSpecRule"])

				if specRulesLen == 1:	# should print at same line as upgrade name
					self.writeSingleLineSpecRules(iOption, gain, gainIndex, tmpCost, a_position, makeStep, writePoints)
				elif specRulesLen >= 2:	### should be check for triplets length
					self.writeTripletsSpecRules(iOption, gain, gainIndex, tmpCost, a_position, makeStep, writePoints)

				elif specRulesLen == 0:
					stringToWrite = gain["gainName"]
					self.writeText(a_position.x, a_position.y, stringToWrite, 8)
					writePoints(tmpCost, a_position.x, a_position.y)
					makeStep()


			self.pdf.line(a_position.x + 2, a_position.y - 2, a_position.x + 38, a_position.y - 2)

		goToNextPage()
