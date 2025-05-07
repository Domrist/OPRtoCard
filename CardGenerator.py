from fpdf import FPDF

from contants import *

from fpdf import FPDF


class CardGenerator:

	pdf : FPDF

	def __init__(self, a_fpdf):
		self.pdf = a_fpdf

	def writeText(self, x, y, text, sizee = 10,  sstyle = ''):
		if sstyle:
			self.pdf.set_font(family = "Helvetica", style = sstyle, size = sizee)
		else:
			self.pdf.set_font(family = "Helvetica", size = sizee)

		self.pdf.set_xy(x,y)
		self.pdf.write(0,text)


	def writeCenteredText(self, x, y, text, sizee=10):
		if x < 0:
			print("LESS")
		self.pdf.set_font(family = "Helvetica", size = sizee)
		textLength = self.pdf.get_string_width(text)

		x -= (textLength/2)

		x -= (self.pdf.c_margin)	# EVERY TEXT HAVE MARGIN

		self.pdf.set_xy(x,y)
		self.pdf.write(0,text)


	def fillTest(self):
		sss = "0123456789"
		self.writeText(40, 4, sss, 10)
		print(len(sss))


	### API DATA WRITER
	def writeFirstHeroCardData(self, a_unitData, a_rowIndex):

		baseRowY = a_rowIndex * DEFAULT_CARD_HEIGHT

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


		def checkEndPage():
			nonlocal cardRowBalance
			if cardRowBalance <= 0:
				cardRowBalance = 12
				a_position.y = 4
				a_position.x += DEFAULT_CARD_WIDTH


		def makeRowStep():
			nonlocal cardRowBalance
			nonlocal cardRowBalance

			a_position.y += STEP_LINE_GLOBAL
			cardRowBalance -= 1


		def makeStep():
			makeRowStep()
			checkEndPage()


		def goToNextPage():
			a_position.x += DEFAULT_CARD_WIDTH
			a_position.y = 4


		# print header data
		headerStrings = []
		if AND_STRING in upgrade["upgradeName"]:
			headerStrings = upgrade["upgradeName"].split(AND_STRING)
			headerStrings[1] = AND_STRING + " " + headerStrings[1]
			headerStrings[1] = headerStrings[1][1:]
		else:
			headerStrings.append(upgrade["upgradeName"])

		for headerString in headerStrings:
			self.writeText(a_position.x, a_position.y, headerString, 8, 'B')
			makeStep()
		# end print header data

		# write gains
		for gain in upgrade["gains"]:
			if len(gain["gainSpecRule"]) < 2:	# should print at same line as upgrade name

				stringToWrite = gain["gainName"] + "(" + gain["gainSpecRule"][0] + ")"
				#print(stringToWrite, " -> ", len(stringToWrite))
				if len(stringToWrite) > MAX_STRING_LENGTH:
					for st in [gain["gainName"], ("(" + gain["gainSpecRule"][0] + ")")]:
						print(st)
						self.writeText(a_position.x, a_position.y, st, 8)
						makeStep()
				else:
					self.writeText(a_position.x, a_position.y, stringToWrite, 8)
					makeStep()
			else:
				stringToWrite = gain["gainName"]
				self.writeText(a_position.x, a_position.y, stringToWrite, 8)
				makeStep()

				triples = fromCollectionToStringifyTriplets(gain["gainSpecRule"])

				for triple in triples:
					stringToWrite = triple
					self.writeText(a_position.x, a_position.y, stringToWrite, 8)
					makeStep()
			self.pdf.line(a_position.x + 2, a_position.y - 2, a_position.x + 38, a_position.y - 2)
		# end write gains - and also end write of upgrade

		goToNextPage()

