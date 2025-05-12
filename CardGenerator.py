from fpdf import FPDF

from contants import *

from fpdf import FPDF


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

		print("Incoming string to split -> ", a_string)
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

		print("SPlitted res => ", tmpArr)

		return tmpArr




	### API DATA WRITER
	def writeFirstHeroCardData(self, a_unitData):

		baseRowY = self.yRowScalerPerPage * DEFAULT_CARD_HEIGHT

		global GLOBAL_X_POS

		GLOBAL_X_POS = 40

		self.writeCenteredText(20, 4 + baseRowY, a_unitData["name"], 9)
		self.writeCenteredText(20, DEFAULT_ROW_COUNT_PER_PAGE + baseRowY, a_unitData["quaDef"], 14)

		self.pdf.line(0, 15 + baseRowY, 40, 15 + baseRowY)

		# генерация кейвордов
		heightShift = 20 + baseRowY

		for keywordTriplet in a_unitData["unitTrinkets"]:
			self.writeCenteredText(20, heightShift, keywordTriplet, 8)
			heightShift += STEP_LINE_GLOBAL

		for weaponData in a_unitData["weaponsData"]:
			self.writeText(0, heightShift, weaponData["weaponName"], 8)
			heightShift += STEP_LINE_GLOBAL
			for weaponTrinketsLine in weaponData["trinkets"]:
				self.writeText(0, heightShift, weaponTrinketsLine, 8)
				heightShift += STEP_LINE_GLOBAL



	def writeUpgradeHeroData(self, a_upgrade, a_position):

		cardRowBalance = DEFAULT_ROW_COUNT_PER_PAGE

		upgrade = a_upgrade

		#a_position.y = 4 + DEFAULT_CARD_HEIGHT * self.yRowScalerPerPage

		def checkEndPage():
			nonlocal cardRowBalance
			if cardRowBalance <= 0:
				cardRowBalance = 12
				a_position.y = 4 + DEFAULT_CARD_HEIGHT * self.yRowScalerPerPage
				a_position.x += DEFAULT_CARD_WIDTH


		def makeRowStep():
			nonlocal cardRowBalance

			a_position.y += STEP_LINE_GLOBAL
			cardRowBalance -= 1


		def makeStep():
			makeRowStep()
			checkEndPage()


		def goToNextPage():
			nonlocal cardRowBalance
			a_position.y = 4 + DEFAULT_CARD_HEIGHT * self.yRowScalerPerPage
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


		for headerString in headerStrings:
			self.writeText(a_position.x, a_position.y, headerString, headerTextFontSize, 'B')
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

					stringToWrite = gain["gainName"] + "(" + gain["gainSpecRule"][0] + ")"
					print("STRING to write -> ", stringToWrite)
					if len(stringToWrite) > MAX_STRING_LENGTH:
						#tmpArr = [gain["gainName"], (gain["gainSpecRule"][0])]
						tmpArr = [gain["gainName"]]

						if self.getTextWidth(gain["gainSpecRule"][0], 8) > (DEFAULT_CARD_WIDTH-5):
							tmpArr += self.splitSingleGainWithBraces(gain["gainSpecRule"][0])
							pass
						else:
							tmpArr += gain["gainSpecRule"][0]

						for st in range(len(tmpArr)):

							self.writeText(a_position.x, a_position.y, tmpArr[st], 8)

							if st == (len(tmpArr)-1) and gainIndex == len(iOption["gains"]) -1:
								print(("TEXT {0} -> SIZE -> {1}").format(tmpArr[st], self.getTextWidth(tmpArr[st], 8)))
								writePoints(tmpCost, a_position.x, a_position.y)
							makeStep()
					else:
						self.writeText(a_position.x, a_position.y, stringToWrite, 8)
						writePoints(tmpCost, a_position.x, a_position.y)
						makeStep()

				elif specRulesLen >= 2:
					stringToWrite = gain["gainName"]
					self.writeText(a_position.x, a_position.y, stringToWrite, 8)
					makeStep()

					triples = fromCollectionToStringifyTriplets(gain["gainSpecRule"])

					for tripleIndex in range(len(triples)):
						stringToWrite = triples[tripleIndex]
						self.writeText(a_position.x, a_position.y, stringToWrite, 8)
						if tripleIndex == (len(triples)-1) and gainIndex == (len(iOption["gains"]) -1):
							writePoints(tmpCost, a_position.x, a_position.y)
						makeStep()

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
