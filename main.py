import json
import os
from CardGenerator import *


directory = os.getcwd() + "/JSONCollectoin/"

pdf.add_page(orientation = "L", format = "a4")
page_height_page = 0
yRowPageIndex = 0


def createPrintableFromSingles():
	for file in os.listdir(directory):
		tmpFilePath = directory+file

		with open(tmpFilePath, 'r') as heroData:
			data = heroData.read()
			obj = json.loads(data)

			unitData = initHerCardData(obj)

			# генерация основных рамок для карточек
			for i in range(unitData.getUnitDataPageCount()):
				pdf.rect(40 * i, yRowPageIndex * DEFAULT_CARD_HEIGHT, DEFAULT_CARD_WIDTH, DEFAULT_CARD_HEIGHT)

			writeHeroCardData(unitData, yRowPageIndex)
			page_height_page += DEFAULT_CARD_HEIGHT
			yRowPageIndex += 1

			if yRowPageIndex >= 3:
				pdf.add_page(orientation = "L", format = "a4")
				page_height_page = 0
				yRowPageIndex = 0



def createPrintableFromGlobal():

	global yRowPageIndex
	global page_height_page

	GLOBAL_JSON = "PLAGUE.json"

	tmpFilePath = directory+GLOBAL_JSON

	with open(tmpFilePath, 'r') as heroData:
		data = heroData.read()
		obj = json.loads(data)

		for tmpUnitDataIndex in range(len(obj)):
			#print(obj[tmpUnitDataIndex])
			unitData = initHerCardData(obj[tmpUnitDataIndex])

			# генерация основных рамок для карточек
			for i in range(unitData.getUnitDataPageCount()):
				pdf.rect(40 * i, yRowPageIndex * DEFAULT_CARD_HEIGHT, DEFAULT_CARD_WIDTH, DEFAULT_CARD_HEIGHT)

			writeHeroCardData(unitData, yRowPageIndex)
			page_height_page += DEFAULT_CARD_HEIGHT
			yRowPageIndex += 1

			if yRowPageIndex >= 3:
				pdf.add_page(orientation = "L", format = "a4")
				page_height_page = 0
				yRowPageIndex = 0


#createPrintableFromGlobal()

#pdf.output("simple_demo.pdf")


import requests
#'https://army-forge.onepagerules.com/api/army-books/FF4UemWHh60T1VRq?gameSystem=5'
x = requests.get('https://army-forge.onepagerules.com/api/army-books/cF1dpwd4bhYsNhsf?gameSystem=5')

obj = json.loads(x.content)
units = obj["units"]

#for key,val in obj.items():
#	print(key)

upgradePackage = obj["upgradePackages"]

localUnit = units[0]

#localUnit[""]
print(localUnit["name"])
print(localUnit["rules"])
print(localUnit["defense"])
print(localUnit["quality"])
print(localUnit["weapons"])
for unitUpgrade in localUnit["upgrades"]:
	print(unitUpgrade)
	for upgradePack in upgradePackage:
		if upgradePack["uid"] == unitUpgrade:
			print(upgradePack)




for unit in units:
	#print(unit["name"])
	unitRules = unit["rules"]
	#print(unitRules)

#print(units)


