class UnitData:

	pageCount = 0	# by default - for first page
	lineCount = 0

	firstPageStringCollection = {}

	stringCollection = []	# collection of string collection

	gains = []



	def __init__(self):
		self.firstPageStringCollection["unitName"] = ""
		self.firstPageStringCollection["quadef"] = ""
		self.firstPageStringCollection["keywords"] = []
		self.firstPageStringCollection["weapons"] = []


	def addFirstPageStrings(self, a_firstPageStrings):
		self.firstPageStringCollection = a_firstPageStrings



	def addUpgradeStrings(self, a_incomingUpgrade):
		self.stringCollection.append(a_incomingUpgrade)



	def addGains(self, a_gain):
		self.gains.append(a_gain)



	def finalPageCountCalculate(self):
		# some some some calculations
		self.pageCount += 1

